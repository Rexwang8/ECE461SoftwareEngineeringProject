import sys
import time

#get args
def main():
    log("Starting main")
    log("Test log")
    str = f"Number of arguments: {len(sys.argv)} arguments."
    log(str)
    str = f"Argument List: {sys.argv}"
    log(str)
    log("Exiting main")
    log("--------------------")
    return 0

def log(msg, priority=0):
    with open("log.txt", "a") as f:
        f.write(f"[Python Main Script] Priority: {priority} | Logging at t={time.time()}: {msg}\n")
        f.close()
        
main()