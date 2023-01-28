import sys
import time
import pathlib
import logger #logger.py


#get args
def main():
    #current working dir
    dir = pathlib.Path().absolute()
    
    
   
    #log("Starting main script...", 1, "log.txt")
    #get first arg as command
    command = sys.argv[1]
    #get second arg LOG LEVEL
    loglevel = sys.argv[2]
    #get third arg as log file
    logfile = sys.argv[3]
    
    #append "log.txt" to current working dir variable
    logpath = str(dir) + "\\" + logfile
    
    Debug = logger.Logger(logpath, 2)
    
    Debug.log("Starting main script...")
    
    logstr = f"ARgS: {sys.argv}, logpath: {logpath}, cmd: {command}, loglevel: {loglevel}"
    Debug.log(logstr, 2)
    
    Debug.log("Starting main script...", 1)

    Debug.log("Testing logging...", 1)
    return 0


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