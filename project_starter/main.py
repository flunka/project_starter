from BitbucketRepo import BitbucketRepo
import subprocess


def git(*args):
  return subprocess.check_call(['git'] + list(args))


def yarn(*args):
  return subprocess.check_call(['yarn'] + list(args))


repo = BitbucketRepo()
project_name = "Test1"
repo_name = "frontend"
# repo.create_project(project_name)
# link = repo.create_repo(project_name, repo_name)
# git('clone', link)
repo.delete_repo(project_name, repo_name)
# repo.delete_project(project_name)
