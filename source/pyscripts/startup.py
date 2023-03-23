import sys
import time
import pathlib
import os
import subprocess

import logger #logger.py
import grader #grader.py
import gitPython #gitPython.py

#get args
def main(loglevel, logfile, inputfile, mode):
    #current working dir
    dir = pathlib.Path().absolute()
    '''
    #get first arg LOG LEVEL
    loglevel = sys.argv[1]
    #get second arg as log file
    logfile = sys.argv[2]
    #get third arg as all input packages
    inputfile = sys.argv[3]
    '''
    Debug = logger.Logger(logfile, 2, "Main")
    #print("dir: " + str(dir))
    #print("loglevel: " + str(loglevel))
    #print("logfile: " + str(logfile))

    Debug.log("HELLO" + mode)
    Debug.log("starting main script...", 1)
    #if repo folder exists, delete it
    if os.path.exists("data/repo"):
        #delete repo folder even if it has files
        os.system("rm -rf data/repo")
    os.mkdir("data/repo")
    
    #we get a list of all packages from arg 3
    packages = ParseInput(inputfile, Debug)
    #print(packages)
    
    #we loop through the list of packages and pull them down
    for package in packages:
        #we sleep for 0.25 seconds to avoid rate limiting
        time.sleep(0.25)

        if (mode == "test"):
            pathToRepo = "UnitTest/testrepo/" + package[0]
            gitPython.pythonGit.pyClone(url=package[2], path=pathToRepo)
        else:
            pathToRepo = "data/repo/" + package[0]

            if(package[1] == "github"):
                Debug.log(f"Cloning {package[0]} from github...", 1)
                gitPython.pythonGit.pyClone(url=package[2], path=pathToRepo)
            elif(package[1] == "npm"):
                #we can find the json at npmdata folder/(name of package).json
                name = package[0]
                npmjson = grader.ImportJSON(f"data/npm/{name}.json")
                githuburl = npmjson["repository"]["url"]
                #clean up url
                githuburl = githuburl.replace("git+", "").replace(".git", "").replace("ssh://", "https://").replace("git://", "https://").replace("git@", "")
                gitPython.pythonGit.pyClone(url=githuburl, path=pathToRepo)
    
    #we now pass to the static analysis tool with c#, exe log level and log file
    #os.system(f"./StaticAnalysisTester {loglevel} {logfile}")
    restdout=subprocess.check_output(f"./StaticAnalysisTester {loglevel} {logfile}", shell=True).decode("utf-8")
    print(f"{restdout}")
    Debug.log(f"./StaticAnalysisTester {loglevel} {logfile}", 1)
    Debug.log("Exiting main script...", 1)

    return 0


    
def MakeFolderRepo(Logger):
    #We make a folder called repo in the current working directory to store the downloaded repo
    
    #check if folder exists
    if(os.path.exists("repo")):
        Logger.log(f"Repo folder already exists at {pathlib.Path().absolute()}", 2)
        return
    os.mkdir("repo")
    Logger.log(f"Repo folder created at {pathlib.Path().absolute()}", 2)
    return
    
def MakeFolderResults(Logger):
    #We make a folder called results in the current working directory to store the results
    
    #check if folder exists
    if(os.path.exists("results")):
        Logger.log(f"Results folder already exists at {pathlib.Path().absolute()}", 2)
        return
    os.mkdir("results")
    Logger.log(f"Results folder created at {pathlib.Path().absolute()}", 2)
    return

def ParseInput(inputfile, Logger):
    #we get a list of all packages from arg 3 by line
    with open(inputfile, 'r') as f:
        packages = f.readlines()
        f.close()   
    Logger.log(f"Recieved {len(packages)} packages from input file.", 2)
    
    ParsedPackages = []
    for package in packages:
        pkgtype = ""
        #we get the package type by checking if it contains a string "github.com"
        if("github.com" in package):
            #this is a github repo
            pkgtype = "github"
        elif("npmjs.com" in package):
            pkgtype = "npm"
        
        #we get the package name by splitting the string by "/"
        pkgname = package.split("/")[-1]
        #we append a tuple of package name, package type, and package url to the list
        ParsedPackages.append((pkgname.replace("\n", ""), pkgtype.replace("\n", ""), package.replace("\n", "")))
    return ParsedPackages
        
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
