from Repo import Repo

import requests
from requests.auth import HTTPBasicAuth
import os


class BitbucketRepo(Repo):
  """docstring for BitbucketRepo"""
  URL = "https://api.bitbucket.org"

  def __init__(self, team=None, user=None, password=None):
    self.user = os.environ.get('BITBUCKET_USER') or user
    self.password = os.environ.get('BITBUCKET_PASSWORD') or password
    self.team = os.environ.get('BITBUCKET_TEAM') or team

  def create_project(self, project_name):
    print("Creating Bitbucket project...")
    data = {
        "name": f"{project_name}",
        "key": f"{project_name}",
        "description": f"Description for {project_name}",
        "is_private": True
    }
    response = requests.post(f'{BitbucketRepo.URL}/2.0/teams/{self.team}/projects/',
                             json=data,
                             auth=(self.user, self.password))
    if response.status_code == 201:
      print(f"Project {project_name} has been created.")
    else:
      print_error(response)

  def create_repo(self, project_name, repo_name="repository"):
    print(f"Checking if {project_name} exists...")
    if self.project_exists(project_name) is False:
      print(f"Project {project_name} does not exist.")
      return -1
    repo_name = f"{project_name.lower()}-{repo_name.lower()}"
    print(f"Creating {repo_name} repository...")
    data = {
        "scm": "git",
        "is_private": True,
        "project": {
            "key": f"{project_name}"
        }
    }
    response = requests.post(f"{BitbucketRepo.URL}/2.0/repositories/{self.team}/{repo_name}",
                             json=data,
                             auth=(self.user, self.password))
    if response.status_code == 200:
      print(f"Repository {repo_name} has been created.")
      clone_link = response.json()['links']['clone'][0]['href']
      return clone_link
    else:
      print_error(response)

  def delete_project(self, project_name):
    print("Deleting Bitbucket project...")
    response = requests.delete(f"{BitbucketRepo.URL}/2.0/teams/{self.team}/projects/{project_name}",
                               auth=(self.user, self.password))
    if response.status_code == 204:
      print(f'Project {project_name} has been deleted successful')
    else:
      print_error(response)

  def delete_repo(self, project_name, repo_name="repository"):
    print("Deleting frontend repository...")
    repo_name = f"{project_name.lower()}-{repo_name.lower()}"
    response = requests.delete(f"{BitbucketRepo.URL}/2.0/repositories/{self.team}/{repo_name}",
                               auth=(self.user, self.password))
    if response.status_code == 204:
      print(f"Repository {repo_name} has been deleted successful")
    else:
      print_error(response)

  def project_exists(self, project_name):
    response = requests.get(f"{BitbucketRepo.URL}/2.0/teams/{self.team}/projects/{project_name}",
                            auth=(self.user, self.password))
    if response.status_code == 200:
      return True
    elif response.status_code == 404:
      return False
    else:
      print_error(response)
      return False


def print_error(response):
  message = response.json()['error']['message']
  print("Somethig has gone wrong...")
  print(f"Status code: {response.status_code}")
  print(f'Message: {message}')
