#Script that provides a logger class for logging to a file
import os
import sys
import pathlib
import time


class Logger:
    def __init__(self, path="log.txt", internalpriority=0, name="Logger Default Name"):
        self.path = path
        self.scriptname = name
        self.internalpriority = internalpriority
        self.log("Logger initialized", 1)
        
    def setpriority(self, priority):
        self.internalpriority = priority
        
    def setpath(self, path):
        self.path = path
        
    def setscriptname(self, name):
        self.scriptname = name
        
    def log(self, msg, priority=0):
        #0 means no logging, 1 is info, 2 is debug and info
        #if priority is 0, return
        if(priority == 0 or self.internalpriority == 0):
            return

        #if message is debug and priority is info, return
        if(self.internalpriority == 1 and priority == 2):
            return
        
	#check if log file exists
        if(not pathlib.Path(self.path).exists()):
            with open(self.path, "w") as f:
                f.write(f"[Python {self.scriptname} Script] Log file created\n")
                f.close()
        
        with open(self.path, "a") as f:
            if(priority == 1):
                f.write(f"[Python {self.scriptname} Script] Priority: {priority}(info) | Logging at t={time.time()}: {msg}\n")
                f.close()
                return
            if(priority == 2):
                
                f.write(f"[Python {self.scriptname} Script] Priority: {priority}(debug) | Logging at t={time.time()}: {msg}\n")
                f.close()
                return
