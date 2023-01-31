import sys
import time
import pathlib
import os

import logger #logger.py
import grader #grader.py

#get args
def main():
    #current working dir
    dir = pathlib.Path().absolute()

   
    #get first arg as command
    command = sys.argv[1]
    #get second arg LOG LEVEL
    loglevel = sys.argv[2]
    #get third arg as log file
    logfile = sys.argv[3]
    #get fourth arg as the URL if it exists
    url = "_"
    if(len(sys.argv) > 4):
        url = sys.argv[4]
    
    #append "log.txt" to current working dir variable
    logpath = str(dir) + "\\" + logfile
    

    Debug = logger.Logger(logpath, 2, "Main")
    
    logstr = f"ARGS: {sys.argv}, logpath: {logpath}, cmd: {command}, loglevel: {loglevel} url: {url}"
    Debug.log(logstr, 2)
    
    Debug.log("Starting main script...", 1)
    
    MakeFolderCache(Debug)
    MakeFolderRepo(Debug)
    MakeFolderResults(Debug)
    
    
    #we check if command is install
    if(command == "install"):
        #command is install
        Debug.log("Recieved command: install, already run by C# parser, exiting python script.", 1)
    elif(command == "build"):
        #command is build
        Debug.log("Recieved command: build, already run by C# parser, exiting python script.", 1)
    elif(command == "test"):
        #this is where we test the loaded packages
        Debug.log("Recieved command: test, Testing loaded packages...", 1)
        pass
    else:
        #this is where we call our api analysis script with the URLS
        Debug.log(f"Recieved command: run, URL recieved is {url}", 1)
        pass
        

    return 0


def MakeFolderCache(Logger):
    #We make a folder called cache in the current working directory to store data
    
    #check if folder exists
    if(os.path.exists("cache")):
        Logger.log(f"Cache folder already exists at {pathlib.Path().absolute()}", 2)
        return
    os.mkdir("cache")
    Logger.log(f"Cache folder created at {pathlib.Path().absolute()}", 2)
    return
    
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

def SendToGrader(config, npmjsonpath, gitjsonpath, staticjsonpath, logpath, loglevel):
    
    #this is where we send the json files to the grader
    success = grader.GradeJSON(config, npmjsonpath, gitjsonpath, staticjsonpath, logpath, loglevel)


main()