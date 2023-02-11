from git import Repo
class pythonGit:
    def pyClone(url, path):
        try:
            Repo.clone_from(url, path)
            #print("Clone success!")
        except:
            #print(f"Clone failed for {url}! error: {sys.exc_info()[0]}")
            pass
        

if __name__ == "__main__":
    pythonGit.pyClone("https://github.com/nullivex/nodist", "/home/shay/a/lin1285/ECE461SoftwareEngineeringProject/testing2")
