#This script takes the path of a number of JSON files (one form npm, one from github, one from the static analysis module) and outputs a NDJSON scoresd file
import json
import logger #logger.py
import datetime


#the final score object
class Score:
    def __init__(self, busFactor=0, rampUp=0, correctness=0, responsiveMaintainer=0, denominator=0, license='MIT'):
        self.busFactor = busFactor
        self.rampUp = rampUp
        self.correctness = correctness
        self.responsiveMaintainer = responsiveMaintainer
        self.license = license
        self.licenseScore = 0
        self.lastUpdated = datetime.datetime.now()
        self.denominator = denominator
    
    #this function is used for debugging
    def __str__(self) -> str:
        return f"Bus Factor: {self.busFactor}\nNet Score: {self.netScore}\nRamp Up: {self.rampUp}\nResponsive Maintainer: {self.responsiveMaintainer}\nLicense: {self.license}\nDenominator: {self.denominator}"
    
    #this function is used to modify the denominator of the score
    def ModifyDenominator(self, value):
        self.denominator += value
        return
    
    def ApplyDenominator(self):
        self.busFactor = self.busFactor / self.denominator
        self.rampUp = self.rampUp / self.denominator
        self.correctness = self.correctness / self.denominator
        self.responsiveMaintainer = self.responsiveMaintainer / self.denominator
        return

    def NormalizeScores(self):
        pass
    
    def CalculateLicenseScore(self):
        pass
    
    def CalculateNetScore(self):
        pass
    
    def CalculateLicenseScore(self):
        pass
    


  
  #structured holder of the npm response      
class npmResponse:
    def __init__(self, name='DefaultName', date=datetime.datetime.now(), npmurl='NPMURL', gitrepo='GITURL', author='DefaultAuthor', maintainers=1, flags={}, npmScores={}):
        self.name = name
        self.date = date
        self.npmurl = npmurl
        self.gitrepo = gitrepo
        self.author = author
        self.maintainers = maintainers
        self.flags = flags
        self.npmScores = npmScores
        
    def __str__(self) -> str:
        return f"Name: {self.name}\nDate: {self.date}\nnpm url: {self.npmurl}\nGit repo: {self.gitrepo}\nAuthor: {self.author}\nMaintainers: {self.maintainers}\nFlags: {self.flags}\nNPM Scores: {self.npmScores}"
        
  #structured holder of the npm response      
class gitResponse:
    def __init__(self, reponame='DefaultName', updateddate=datetime.datetime.now(), diskusage=0, license='MIT', isempty=False, isdisabled=False, isfork=False, isprivate=False, issues=0, forkcount=0, stargazers=0):
        self.reponame = reponame
        self.updateddate = updateddate
        self.diskusage = diskusage
        self.license = license
        self.isempty = isempty
        self.isdisabled = isdisabled
        self.isfork = isfork
        self.isprivate = isprivate
        self.issues = issues
        self.forkcount = forkcount
        self.stargazers = stargazers
        
    def __str__(self) -> str:
        response = f"Repo Name: {self.reponame}\nUpdated Date: {self.updateddate}\nDisk Usage: {self.diskusage}\nLicense: {self.license}\nIs Empty: {self.isempty}\nIs Disabled: {self.isdisabled}\nIs Fork: {self.isfork}\nIs Private: {self.isprivate}\nIssues: {self.issues}\nFork Count: {self.forkcount}\nStargazers: {self.stargazers}"
        return response

#turn a raw json for npm into a gitResponse object
def ParseGitJSON(data):
    if(data == None):
        return None
    
    reponame = data['data']['repository']['name']
    updatedAt = datetime.datetime.strptime(data['data']['repository']['updatedAt'], "%Y-%m-%dT%H:%M:%SZ")
    diskUsage = data['data']['repository']['diskUsage']
    license = data['data']['repository']['licenseInfo']
    isempty = data['data']['repository']['isEmpty']
    isfork = data['data']['repository']['isFork']
    isprivate = data['data']['repository']['isPrivate']
    isdisabled = data['data']['repository']['isDisabled']
    issues = data['data']['repository']['issues']['totalCount']
    forkcount = data['data']['repository']['forkCount']
    stargazers = data['data']['repository']['stargazers']['totalCount']
    
    
    
    resp = gitResponse(reponame=reponame, updateddate=updatedAt, diskusage=diskUsage, license=license, isempty=isempty,
                       isfork=isfork, isprivate=isprivate, isdisabled=isdisabled,
                          issues=issues, forkcount=forkcount, stargazers=stargazers)
    
    return resp

#turn a raw json for npm into a npmResponse object
def ParseNPMJSON(data):
    if(data == None):
        return None
    
    name = data['objects'][0]['package']['name']
    date = datetime.datetime.strptime(data['objects'][0]['package']['date'], "%Y-%m-%dT%H:%M:%S.%fZ")
    links = data['objects'][0]['package']['links']
    authors = data['objects'][0]['package']['author']['name']
    maintainers = data['objects'][0]['package']['maintainers']
    flags = data['objects'][0]['flags']
    scores = data['objects'][0]['score']

    npmscore = npmResponse(name, date, links['npm'], links['repository'], authors, len(maintainers), flags, scores['detail'])
    return npmscore


#filepath to json
def ImportJSON(path):
    with open(path, "r") as f:
        data = json.load(f)
        f.close()
        return data
    
#json back to file
def ExportJSON(data, path):
    with open(path, "w") as f:
        json.dump(data, f)
        f.close()
        return
    
    
def GradeNPM(data, score):
    #we assume data is valid, we will go by category
    score.busFactor += 100
    score.responsiveMaintainer += 100
    score.rampUp += 100
    score.license = 'MIT'
    score.correctness += 100
    
    #we parse flags and assign a penalty to them
    if(data.flags['deprecated']): #completely deprecated, hard to give it any support
        score.busFactor -= 50
        score.responsiveMaintainer -= 50
        score.correctness -= 50
    elif(data.flags['outdated']): #outdated, but not deprecated, we can still give it some support
        score.busFactor -= 25
        score.responsiveMaintainer -= 25
        score.correctness -= 25
        score.rampUp -= 25
    elif(data.flags['unstable']): #unstable, potentially actively developed, but not stable, things can break or change
        score.responsiveMaintainer -= 15
        score.correctness -= 30
        score.rampUp -= 20
        
        
    return score
    
    
    
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
    score = Score(0, 0, 0, 0, 0, '', denominator=0)
    npmscore = ParseNPMJSON(npmjson)
    
    
    layout = ''
    if(config['npm'] == 'ready'):
        layout += 'npm'
        score.ModifyDenominator(100)
        score = GradeNPM(npmscore, score)
    if(config['github'] == 'ready'):
        layout += 'git'
        score.ModifyDenominator(100)
        
    if(config['static'] == 'ready'):
        layout += 'static'
        score.ModifyDenominator(100)
        
        
    score.NormalizeScores()
    print(score.netScore)
        
    
    return 0


def printjson(data):
    print(json.dumps(data, indent=4, sort_keys=True))
    
def logjson(data, DebugLogger):
    DebugLogger.log(json.dumps(data, indent=4, sort_keys=True), 2)
    
     
def main():
    #test main to check stuff works
    #import the json files
    npmjson = ImportJSON("npmex.json")
    npmscore = ParseNPMJSON(npmjson)
    
    gitjson = ImportJSON("github_api/data/cloudinary.json")
    gitscore = ParseGitJSON(gitjson)
    
    ExportJSON(npmjson, "npm.json")
    ExportJSON(gitjson, "git.json")
    
    
    print(str(npmscore))
    print(str(gitscore))
    

    #json3 = ImportJSON("Build\jsonexample.json")
    Debug = logger.Logger("log.txt", 2)
    Debug.log("Testing json import", 2)
    
    logjson(npmjson, Debug)
    logjson(gitjson, Debug)
    
    
    
if __name__ == "__main__":
    main()
    
    