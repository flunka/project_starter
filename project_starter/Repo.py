from abc import ABC, abstractmethod


class Repo(ABC):
  """docstring for Repo"""

  @abstractmethod
  def create_repo(self):
    print("Creating repository...")
    pass

  @abstractmethod
  def delete_repo(self):
    print("Deleting frontend repository...")
    pass
