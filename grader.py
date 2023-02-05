#This script takes the path of a number of JSON files (one form npm, one from github, one from the static analysis module) and outputs a NDJSON scoresd file
import json
import logger #logger.py


class Score:
    def __init__(self, busFactor, netScore, rampUp, responsiveMaintainer, denominator, license):
        self.busFactor = busFactor
        self.netScore = netScore
        self.rampUp = rampUp
        self.responsiveMaintainer = responsiveMaintainer
        self.license = license
        self.denominator = denominator
        

def ImportJSON(path):
    with open(path, "r") as f:
        data = json.load(f)
        f.close()
        return data
    
    
def ExportJSON(data, path):
    with open(path, "w") as f:
        json.dump(data, f)
        f.close()
        return
    
    
def GradeJSON(config, npmjsonpath, gitjsonpath, staticjsonpath, logpath, loglevel):
    #we use the config variable to tell the grader which json files to ignore, if a json file doesn't exist, we ignore it
    npmjson, gitjson, staticjson = None, None, None
    Debug = logger.Logger("Build\log.txt", 2, "Grader")
    Debug.log("Testing json import", 2)
    
    
    #import the json files
    if(config["npm"] == "ignore"):
        npmjsonpath = None
    else:
        npmjson = ImportJSON(npmjsonpath)
        
    if(config["github"] == "ignore"):
        gitjsonpath = None
    else:
        gitjson = ImportJSON(gitjsonpath)
        
    if(config["static"] == "ignore"):
        staticjsonpath = None
    else:
        staticjson = ImportJSON(staticjsonpath)
        
    #we now have the json files loaded, we can now grade them
    #we will figure out which json files we have
    
    #we declare the score object
    score = Score(0, 0, 0, 0, 0, '', 100)
    
    
    layout = ''
    if(config['npm'] == 'ready'):
        layout += 'npm'
        
    if(config['github'] == 'ready'):
        layout += 'git'
    if(config['static'] == 'ready'):
        layout += 'static'
        
    
        
    
    return 0


def printjson(data):
    print(json.dumps(data, indent=4, sort_keys=True))
    
def logjson(data, DebugLogger):
    DebugLogger.log(json.dumps(data, indent=4, sort_keys=True), 2)
    
     
def main():
    #test main to check stuff works
    #import the json files
    json1 = ImportJSON("Build\jsonexample.json")
    json2 = ImportJSON("Build\jsonexample.json")
    json3 = ImportJSON("Build\jsonexample.json")
    Debug = logger.Logger("Build\log.txt", 2)
    Debug.log("Testing json import", 2)
    print(json1)
    
    
if __name__ == "__main__":
    main()
    
    