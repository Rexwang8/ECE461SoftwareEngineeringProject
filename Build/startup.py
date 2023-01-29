import sys
import time
import pathlib

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
    
    #we check if command is install
    if(command == "install"):
        #command is install
        Debug.log("Recieved command: install, already run by C# parser, exiting python script.", 1)
    elif(command == "build"):
        #command is build
        Debug.log("Recieved command: build, already run by C# parser, exiting python script.", 1)
    elif(command == "run"):
        #this is where we call our api analysis script with the URLS
        Debug.log(f"Recieved command: run, URL recieved is {url}", 1)
        pass
    elif(command == "test"):
        #this is where we test the loaded packages
        Debug.log("Recieved command: test, Testing loaded packages...", 1)
        pass
        

    return 0


def SendToGrader(config, npmjsonpath, gitjsonpath, staticjsonpath, logpath, loglevel):
    
    #this is where we send the json files to the grader
    success = grader.GradeJSON(config, npmjsonpath, gitjsonpath, staticjsonpath, logpath, loglevel)

'''
def log(msg, priority=0, path="log.txt"):
    if(priority == 0):
        return
    
    #check if log file exists
    if(not pathlib.Path(path).exists()):
        with open(path, "w") as f:
            f.write("[Python Main Script] Log file created\n")
            f.close()
    
    with open(path, "a") as f:
        f.write(f"[Python Main Script] Priority: {priority} | Logging at t={time.time()}: {msg}\n")
        f.close()

        '''

main()