from git import Repo

class pythonGit:
    def pyClone(url, path):
        Repo.clone_from(url, path)