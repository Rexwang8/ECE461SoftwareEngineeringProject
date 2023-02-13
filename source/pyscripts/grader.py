#This script takes the path of a number of JSON files (one form npm, one from github, one from the static analysis module) and outputs a NDJSON scoresd file
import json
import logger #logger.py
import datetime
import os
import sys


#the final score object
class Score:
    def __init__(self, busFactor=0, rampUp=0, correctness=0, responsiveMaintainer=0, denominator=0, license='MIT', netScore=0, licenseScore=0, lastUpdated=datetime.datetime.now(), url="", pkgName=""):
        self.busFactor = busFactor
        self.rampUp = rampUp
        self.correctness = correctness
        self.responsiveMaintainer = responsiveMaintainer
        self.license = license
        self.licenseScore = licenseScore
        self.lastUpdated = datetime.datetime.now()
        self.denominator = denominator
        self.netScore = netScore
        self.url = url
        self.pkgName = ""
    
    #this function is used for debugging
    def __str__(self) -> str:
        return f"Bus Factor: {self.busFactor}\nRamp Up: {self.rampUp}\nCorrectness: {self.correctness}\nResponsive Maintainer: {self.responsiveMaintainer}\nLicense: {self.license}\nLicense Score: {self.licenseScore}\nLast Updated: {self.lastUpdated}\nDenominator: {self.denominator}"
    
    #this function is used to modify the denominator of the score
    def ModifyDenominator(self, value):
        self.denominator += value
        return
    
    
    
    def CalculateNetScore(self):
        #weighting of each score
        self.netScore = ((self.busFactor * 0.15) + (self.rampUp * 0.15) + (self.correctness * 0.15) + (self.responsiveMaintainer * 0.35) + (self.licenseScore * 0.2)) / self.denominator
        pass
    

    


  
  #structured holder of the npm response      
class npmResponse:
    def __init__(self, name='DefaultName', date=datetime.datetime.now(), gitrepo='GITURL', author='DefaultAuthor', maintainers=1, license='MIT', versionCount=1, readmelen=0):
        self.name = name
        self.date = date
        self.gitrepo = gitrepo
        self.author = author
        self.maintainers = maintainers
        self.license = license
        self.versionCount = versionCount
        self.readmelen = readmelen
        
    def __str__(self) -> str:
        return f"Name: {self.name}\nDate: {self.date}\nGit repo: {self.gitrepo}\nAuthor: {self.author}\nMaintainers: {self.maintainers}\nLicense: {self.license}\nVersion Count: {self.versionCount}\nReadme Length: {self.readmelen}"
        
  #structured holder of the npm response      
class gitResponse:
    def __init__(self, reponame='DefaultName', updateddate=datetime.datetime.now(), diskusage=0, license='MIT', isempty=False, isdisabled=False, isfork=False, isprivate=False, issues=0, forkcount=0, stargazers=0, openIssues=0):
        self.reponame = reponame
        self.updateddate = updateddate
        self.diskusage = diskusage
        self.license = license
        self.isempty = isempty
        self.isdisabled = isdisabled
        self.isfork = isfork
        self.isprivate = isprivate
        self.issues = issues
        self.openIssues = openIssues
        self.forkcount = forkcount
        self.stargazers = stargazers
        
    def __str__(self) -> str:
        response = f"Repo Name: {self.reponame}\nUpdated Date: {self.updateddate}\nDisk Usage: {self.diskusage}\nLicense: {self.license}\nIs Empty: {self.isempty}\nIs Disabled: {self.isdisabled}\nIs Fork: {self.isfork}\nIs Private: {self.isprivate}\nIssues: {self.issues}\nFork Count: {self.forkcount}\nStargazers: {self.stargazers}"
        return response

class staticResponse:
    def __init__(self, codeLineCount=0, commentLineCount=0, codeCharCount=0, commentCharCount=0, licensePath='', readmePath='', license='MIT', licenseCompatibility=0):
        self.codeLineCount = codeLineCount
        self.commentLineCount = commentLineCount
        self.codeCharCount = codeCharCount
        self.commentCharCount = commentCharCount
        self.licensePath = licensePath
        self.readmePath = readmePath
        self.license = license
        self.licenseCompatibility = licenseCompatibility
        
    def __str__(self) -> str:
        response = f"Code Line Count: {self.codeLineCount}\nComment Line Count: {self.commentLineCount}\nCode Char Count: {self.codeCharCount}\nComment Char Count: {self.commentCharCount}\nLicense Path: {self.licensePath}\nReadme Path: {self.readmePath}\nLicense: {self.license}\nLicense Compatibility: {self.licenseCompatibility}"
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
    openissues = data['data']['repository']['openIssues']['totalCount']
    forkcount = data['data']['repository']['forkCount']
    stargazers = data['data']['repository']['stargazers']['totalCount']
    
    
    
    resp = gitResponse(reponame=reponame, updateddate=updatedAt, diskusage=diskUsage, license=license, isempty=isempty,
                       isfork=isfork, isprivate=isprivate, isdisabled=isdisabled,
                          issues=issues, forkcount=forkcount, stargazers=stargazers,
                          openIssues=openissues)
    
    return resp

#turn a raw json for npm into a npmResponse object
def ParseNPMJSON(data):
    if(data == None):
        return None
    
    name = data['name']
    alltimes = data['time']
    
    #set to 1970
    latesttime = datetime.datetime(1970, 1, 1)
    #convert alltimes to a list of datetimes and get the latest that isn't ['modified']
    for time in alltimes:
        if time != 'modified':
            date = datetime.datetime.strptime(alltimes[time], "%Y-%m-%dT%H:%M:%S.%fZ")
            if date > latesttime:
                latesttime = date
                
                
    date = latesttime
    links = data['repository']['url'].replace('git+', '').replace('.git', '').replace('git://', 'https://').replace('ssh://', 'https://').replace('git@', '')
    authors = data['author']['name']
    maintainers = data['maintainers']
    license = data['license']
    versionCount = len(data['versions'])
    readmelen = len(data['readme'])

    npmscore = npmResponse(name, date, links, authors, len(maintainers), license, versionCount,readmelen)
    return npmscore

def ParseStaticJSON(data):
    if data == None:
        return None
    
    codeLineCount = data['codeLineCount']
    commentLineCount = data['commentLineCount']
    codeCharCount = data['codeCharCount']
    commentCharCount = data['commentCharCount']
    licensePath = data['licensePath']
    readmePath = data['readmePath']
    license = str(data['license']).replace(' ', '').lower().strip()
    compatibility = data['licenseCompatibility']
    
    return staticResponse(codeLineCount, commentLineCount, codeCharCount, commentCharCount, licensePath, readmePath, license, compatibility)


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
    
def GetScore(pkg, gitList, npmList, staticList, logger):
    finalscore = Score()
    finalscore.name = pkg
    
    
    logger.log("Getting score for " + finalscore.name)
    #print("Getting score for " + finalscore.name)
    

    git = None
    if gitList is not None:
        #check if the package is in the git list
        if pkg + ".json" in gitList.keys():
            git = gitList[pkg + ".json"]
        
    npm = None
    if npmList is not None:
        #check if the package is in the npm list
        if pkg + ".json" in npmList.keys():
            npm = npmList[pkg + ".json"]
            
    static = None
    if staticList is not None:
        static = staticList[pkg + ".json"]
        
    #we first check which files are available
    if git is not None:
        finalscore.ModifyDenominator(100)
    if npm is not None:
        finalscore.ModifyDenominator(100)
    if static is not None:
        finalscore.ModifyDenominator(100)
    
    
    
    #handle license compatibility and license
    if static is not None:
        finalscore.license = static.license
        finalscore.licenseCompatibility = static.licenseCompatibility
    elif git is not None:
        finalscore.license = git.license
        if finalscore.license.toLower() == "mit" or finalscore.license.toLower() == "apache-2.0":
            finalscore.licenseCompatibility = 1
            
    elif npm is not None:
        finalscore.license = npm.license
        if finalscore.license.toLower() == "mit" or finalscore.license.toLower() == "apache-2.0":
            finalscore.licenseCompatibility = 1
    else:
        finalscore.license = "N/A"
        finalscore.licenseCompatibility = 0
    
    #fill in last updated date
    gitlastupdated = datetime.datetime(1970, 1, 1)
    npmlastupdated = datetime.datetime(1970, 1, 1)
    if(git is not None):
        gitlastupdated = git.updateddate
    if(npm is not None):
        npmlastupdated = npm.date
    #compare dates
    if gitlastupdated > npmlastupdated:
        finalscore.lastupdated = gitlastupdated
    else:
        finalscore.lastupdated = npmlastupdated
        
    #bus factor
    if git is not None:
        #20pts if not fork, up to 50 pts for issues, 30 pts for fork count
        #if the repo is empty, it's a 0, if is disabled, it's a 0
        if git.isempty:
            finalscore.busFactor += 0 #empty repo, +0
        elif git.isdisabled:
            finalscore.busFactor += 5 #disabled repo, +5
        elif git.isprivate:
            finalscore.busFactor += 10 #private repo, +10
        elif not git.isfork:
            finalscore.busFactor += 20 #main project, +20
        else:
            finalscore.busFactor += 0 #fills none

        #if the repo has no issues, it's a 10
        if git.issues == 0:
            finalscore.busFactor += 10 #no issues, +10
        #if the repo has 1-15 issues, it's a 20
        elif git.issues <= 15:
            finalscore.busFactor += 20
        #if the repo has 16-30 issues, it's a 30
        elif git.issues <= 30:
            finalscore.busFactor += 30
        #if the repo has 31-60 issues, it's a 40
        elif git.issues <= 60:
            finalscore.busFactor += 40
        #if the repo has 61+ issues, it's a 50
        elif git.issues >= 61:
            finalscore.busFactor += 50
            
        #if the repo has 0 forks, it's a 5
        if git.forkcount == 0:
            finalscore.busFactor += 5
        #if the repo has 1-10 forks, it's a 10
        elif git.forkcount <= 10:
            finalscore.busFactor += 10
        #if the repo has 11-25 forks, it's a 15
        elif git.forkcount <= 25:
            finalscore.busFactor += 15
        #if the repo has 26-50 forks, it's a 20
        elif git.forkcount <= 50:
            finalscore.busFactor += 20
        #if the repo has 51-100 forks, it's a 25
        elif git.forkcount <= 100:
            finalscore.busFactor += 25
        #if the repo has 100+ forks, it's a 30
        elif git.forkcount >= 101:
            finalscore.busFactor += 30
    
    if npm is not None:
        #60 pts for maintainers count 40pts for version count
        if npm.maintainers == 0:
            finalscore.busFactor += 0
        elif npm.maintainers == 1:
            finalscore.busFactor += 5
        elif npm.maintainers == 2:
            finalscore.busFactor += 10
        elif npm.maintainers <= 5:
            finalscore.busFactor += 20
        elif npm.maintainers <= 15:
            finalscore.busFactor += 30
        elif npm.maintainers <= 30:
            finalscore.busFactor += 40
        elif npm.maintainers <= 50:
            finalscore.busFactor += 50
        elif npm.maintainers >= 51:
            finalscore.busFactor += 60
            
        if npm.versionCount == 0:
            finalscore.busFactor += 0
        elif npm.versionCount <= 15:
            finalscore.busFactor += 10
        elif npm.versionCount <= 40:
            finalscore.busFactor += 20
        elif npm.versionCount <= 70:
            finalscore.busFactor += 30
        elif npm.versionCount >= 91:
            finalscore.busFactor += 40
            
    if static is not None:
        #40 pts for last updated date, 50 pts ratio of code to comments, 10 pts for including a readme
        #if the last updated date is within the last 3 months, it's a 40
        if finalscore.lastupdated >= datetime.datetime.now() - datetime.timedelta(days=90):
            finalscore.busFactor += 40
        elif finalscore.lastupdated >= datetime.datetime.now() - datetime.timedelta(days=180):
            finalscore.busFactor += 30
        elif finalscore.lastupdated >= datetime.datetime.now() - datetime.timedelta(days=365):
            finalscore.busFactor += 20
        elif finalscore.lastupdated >= datetime.datetime.now() - datetime.timedelta(days=730):
            finalscore.busFactor += 10
        else:
            finalscore.busFactor += 0
        
        if static.readmePath != "":
            finalscore.busFactor += 10
        
        codeToCommentRatio = static.codeLineCount / static.commentLineCount
        
        #more comments, the better
        if codeToCommentRatio >= 10:
            finalscore.busFactor += 50
        elif codeToCommentRatio >= 15:
            finalscore.busFactor += 40
        elif codeToCommentRatio >= 25:
            finalscore.busFactor += 30
        elif codeToCommentRatio >= 50:
            finalscore.busFactor += 20
        elif codeToCommentRatio >= 100:
            finalscore.busFactor += 10
        else:
            finalscore.busFactor += 0
        
    #rampup
    if git is not None:
        #30 pts for repo status, 20 pts for stargazers, 20 pts for issues, 30 pts for repo size
        #Justification: if repo is in a bad state, it's not a good sign
        # the more stars, the better (more people are using it) - Weighted more since stargazers tend to not be other devs
        # the more issues, the better (more people are using it)
        #if the repo has no commits, it's a 0
        if git.isempty:
            finalscore.rampUp += 0
        elif git.isdisabled:
            finalscore.rampUp += 0
        elif git.isprivate:
            finalscore.rampUp += 10
        elif git.isfork:
            finalscore.rampUp += 15
        else:
            finalscore.rampUp += 30
            
        if git.stargazers <= 10:
            finalscore.rampUp += 0
        elif git.stargazers <= 50:
            finalscore.rampUp += 10
        elif git.stargazers <= 100:
            finalscore.rampUp += 15
        elif git.stargazers <= 200:
            finalscore.rampUp += 20
        elif git.stargazers <= 500:
            finalscore.rampUp += 25
        elif git.stargazers >= 501:
            finalscore.rampUp += 30
            
        if git.issues <= 10:
            finalscore.rampUp += 0
        elif git.issues <= 50:
            finalscore.rampUp += 10
        elif git.issues <= 100:
            finalscore.rampUp += 15
        elif git.issues <= 200:
            finalscore.rampUp += 20
            
        #smaller repos are better (easier to get started)
        if git.diskusage >= 100000:
            finalscore.rampUp += 0
        elif git.diskusage >= 50000:
            finalscore.rampUp += 5
        elif git.diskusage >= 10000:
            finalscore.rampUp += 10
        elif git.diskusage >= 5000:
            finalscore.rampUp += 15
        elif git.diskusage >= 1000:
            finalscore.rampUp += 20
        elif git.diskusage >= 500:
            finalscore.rampUp += 25
        else:
            finalscore.rampUp += 30
            
    if npm is not None:
        #10 pts for readme length, 45 pts for maintainers count, 45 pts for version count
        #JUSITFICATION: the more maintainers, the better (better chance of getting help)
        # the more versions, the better (more people are using it)
        # the longer the readme, the better (easy to get started)
        if npm.readmelen <= 100:
            finalscore.rampUp += 0
        elif npm.readmelen <= 500:
            finalscore.rampUp += 5
        elif npm.readmelen >= 501:
            finalscore.rampUp += 10
        
        if npm.maintainers == 0:
            finalscore.rampUp += 0
        elif npm.maintainers <= 10:
            finalscore.rampUp += 15
        elif npm.maintainers <= 20:
            finalscore.rampUp += 30
        elif npm.maintainers >= 21:
            finalscore.rampUp += 45
            
        if npm.versionCount == 0:
            finalscore.rampUp += 0
        elif npm.versionCount <= 10:
            finalscore.rampUp += 15
        elif npm.versionCount <= 35:
            finalscore.rampUp += 30
        elif npm.versionCount >= 60:
            finalscore.rampUp += 45

    if static is not None:
        #30 pts for last updated date, 30 pts ratio of code to comments, 10 pts for including a readme, 20 pts for a small codebase
        #Justification: the more recent the last update, the better (code is being maintained)
        # the more comments, the better (easier to understand)
        #including a readme is a good sign
        if finalscore.lastupdated >= datetime.datetime.now() - datetime.timedelta(days=90):
            finalscore.rampUp += 30
        elif finalscore.lastupdated >= datetime.datetime.now() - datetime.timedelta(days=180):
            finalscore.rampUp += 15
        elif finalscore.lastupdated >= datetime.datetime.now() - datetime.timedelta(days=365):
            finalscore.rampUp += 10
        elif finalscore.lastupdated >= datetime.datetime.now() - datetime.timedelta(days=730):
            finalscore.rampUp += 5
        else:
            finalscore.rampUp += 0
            
        codeToCommentRatio = static.codeLineCount / static.commentLineCount
        
        if codeToCommentRatio >= 10:
            finalscore.rampUp += 40
        elif codeToCommentRatio >= 15:
            finalscore.rampUp += 30
        elif codeToCommentRatio >= 25:
            finalscore.rampUp += 20
        elif codeToCommentRatio >= 50:
            finalscore.rampUp += 15
        elif codeToCommentRatio >= 100:
            finalscore.rampUp += 5
        else:
            finalscore.rampUp += 0
        
        if static.readmePath != "":
            finalscore.rampUp += 10
            
        if static.codeLineCount <= 1000:
            finalscore.rampUp += 20
        elif static.codeLineCount <= 5000:
            finalscore.rampUp += 15
        elif static.codeLineCount <= 10000:
            finalscore.rampUp += 10
        else:
            finalscore.rampUp += 0
    
    #correctness
    if git is not None:
        #30 pts for repo status, 20 pts for stargarzers, 50 pts for ratio of open issues to closed issues
        #Justification: if repo is in a bad state, it's not a good sign
        # the more stars, the better (more people are using it)
        # the lower the ratio of open issues to closed issues, the better (more issues are being resolved)
        
        if git.isempty:
            finalscore.correctness += 0
        elif git.isdisabled:
            finalscore.correctness += 0
        elif git.isprivate:
            finalscore.correctness += 10
        elif git.isfork:
            finalscore.correctness += 15
        else:
            finalscore.correctness += 30
        
        if git.stargazers <= 10:
            finalscore.correctness += 0
        elif git.stargazers <= 50:
            finalscore.correctness += 10
        elif git.stargazers <= 100:
            finalscore.correctness += 20
        else:
            finalscore.correctness += 20
            
        openToAllIssuesRatio = git.openIssues / git.issues
        
        if openToAllIssuesRatio <= 0.1:
            finalscore.correctness += 50
        elif openToAllIssuesRatio <= 0.2:
            finalscore.correctness += 40
        elif openToAllIssuesRatio <= 0.3:
            finalscore.correctness += 30
        elif openToAllIssuesRatio <= 0.4:
            finalscore.correctness += 20
        elif openToAllIssuesRatio <= 0.5:
            finalscore.correctness += 10
        else:
            finalscore.correctness += 0
    
    if npm is not None:
        #60 pts for maintainers count, 40 pts for version count
        #JUSITFICATION: the more maintainers, the better (better chance of getting help, more people are correcting issues)
        # the more versions, the better (more people are using it)
        if npm.maintainers == 0:
            finalscore.correctness += 0
        elif npm.maintainers <= 12:
            finalscore.correctness += 30
        elif npm.maintainers <= 25:
            finalscore.correctness += 40
        elif npm.maintainers >= 26:
            finalscore.correctness += 60
            
        if npm.versionCount == 0:
            finalscore.correctness += 0
        elif npm.versionCount <= 10:
            finalscore.correctness += 10
        elif npm.versionCount <= 25:
            finalscore.correctness += 20
        elif npm.versionCount <= 50:
            finalscore.correctness += 30
        elif npm.versionCount >= 80:
            finalscore.correctness += 40
            
    if static is not None:
        #30 pts for last updated date, 10 pts for including a readme, 10 pts for including a license, 50 pts for license compatibility
        #Justification: the more recent the last update, the better (code is being maintained)
        # including a readme is a good sign
        # including a license is a good sign
        # if the license is compatible with the project, it's a good sign
        if finalscore.lastupdated >= datetime.datetime.now() - datetime.timedelta(days=90):
            finalscore.correctness += 30
        elif finalscore.lastupdated >= datetime.datetime.now() - datetime.timedelta(days=180):
            finalscore.correctness += 20
        elif finalscore.lastupdated >= datetime.datetime.now() - datetime.timedelta(days=365):
            finalscore.correctness += 10
        elif finalscore.lastupdated >= datetime.datetime.now() - datetime.timedelta(days=730):
            finalscore.correctness += 5
        else:
            finalscore.correctness += 0
            
        if static.readmePath != "":
            finalscore.correctness += 10
        
        if static.licensePath != "":
            finalscore.correctness += 10
            
        if static.licenseCompatibility == 1:
            finalscore.correctness += 50
            
    #responsiveness - measure of how responsive the project is to issues
    
    if git is not None:
        #30 pts for repo status, 20 pts for last updated date, 50 pts for ratio of open issues to closed issues
        #Justification: if repo is in a bad state, it's not a good sign
        # the less the ratio of open issues to closed issues, the better (more issues are being resolved)
        # the more recent the last update, the better (code is being maintained)
        
        if git.isempty:
            finalscore.responsiveMaintainer += 0
        elif git.isdisabled:
            finalscore.responsiveMaintainer += 0
        elif git.isprivate:
            finalscore.responsiveMaintainer += 10
        elif git.isfork:
            finalscore.responsiveMaintainer += 15
        else:
            finalscore.responsiveMaintainer += 30
            
        openToAllIssuesRatio = git.openIssues / git.issues
        
        if openToAllIssuesRatio <= 0.1:
            finalscore.responsiveMaintainer += 50
        elif openToAllIssuesRatio <= 0.2:
            finalscore.responsiveMaintainer += 40
        elif openToAllIssuesRatio <= 0.3:
            finalscore.responsiveMaintainer += 30
        elif openToAllIssuesRatio <= 0.4:
            finalscore.responsiveMaintainer += 20
        elif openToAllIssuesRatio <= 0.5:
            finalscore.responsiveMaintainer += 10
        else:
            finalscore.responsiveMaintainer += 0

        if gitlastupdated >= datetime.datetime.now() - datetime.timedelta(days=90):
            finalscore.responsiveMaintainer += 20
        elif gitlastupdated >= datetime.datetime.now() - datetime.timedelta(days=180):
            finalscore.responsiveMaintainer += 15
        elif gitlastupdated >= datetime.datetime.now() - datetime.timedelta(days=365):
            finalscore.responsiveMaintainer += 10
        elif gitlastupdated >= datetime.datetime.now() - datetime.timedelta(days=730):
            finalscore.responsiveMaintainer += 5
        else:
            finalscore.responsiveMaintainer += 0
            
    if npm is not None:
        #50 pts for last updated date, 50 pts for number of maintainers
        #Justification: the more recent the last update, the better (code is being maintained)
        # the more maintainers, the better (better chance of getting help, more people are correcting issues)
        
        if npm.date >= datetime.datetime.now() - datetime.timedelta(days=90):
            finalscore.responsiveMaintainer += 50
        elif npm.date >= datetime.datetime.now() - datetime.timedelta(days=180):
            finalscore.responsiveMaintainer += 40
        elif npm.date >= datetime.datetime.now() - datetime.timedelta(days=365):
            finalscore.responsiveMaintainer += 30
        elif npm.date >= datetime.datetime.now() - datetime.timedelta(days=730):
            finalscore.responsiveMaintainer += 20
        else:
            finalscore.responsiveMaintainer += 0
            
        if npm.maintainers == 0:
            finalscore.responsiveMaintainer += 0
        elif npm.maintainers <= 10:
            finalscore.responsiveMaintainer += 10
        elif npm.maintainers <= 20:
            finalscore.responsiveMaintainer += 20
        elif npm.maintainers <= 30:
            finalscore.responsiveMaintainer += 30
        elif npm.maintainers <= 50:
            finalscore.responsiveMaintainer += 40
        elif npm.maintainers >= 51:
            finalscore.responsiveMaintainer += 50
        
    if static is not None:
        #50 pts for last updated date, 10 pts for including a readme, 10 pts for including a license, 30 pts for license compatibility
        #Justification: the more recent the last update, the better (code is being maintained)
        # including a readme is a good sign
        # including a license is a good sign
        # if the license is compatible with the project, then its open source, which is a good sign
        if finalscore.lastupdated >= datetime.datetime.now() - datetime.timedelta(days=60):
            finalscore.responsiveMaintainer += 50
        elif finalscore.lastupdated >= datetime.datetime.now() - datetime.timedelta(days=120):
            finalscore.responsiveMaintainer += 35
        elif finalscore.lastupdated >= datetime.datetime.now() - datetime.timedelta(days=200):
            finalscore.responsiveMaintainer += 20
        elif finalscore.lastupdated >= datetime.datetime.now() - datetime.timedelta(days=365):
            finalscore.responsiveMaintainer += 10
        else:
            finalscore.responsiveMaintainer += 0
            
        if static.readmePath != "":
            finalscore.responsiveMaintainer += 10
        
        if static.licensePath != "":
            finalscore.responsiveMaintainer += 10
            
        if static.licenseCompatibility == 1:
            finalscore.responsiveMaintainer += 30
            
        
               
    finalscore.CalculateNetScore()
    return finalscore

#pretty prints a table to the console for the user based on final score broken down by category
def prettyPrintTable(allfinalscores, pkg):
    #dont use prettytable, it's not a dependency
    #print headers: name, net score, license, license compatibility, last updated, bus factor, rampup, correctness, responsiveness, denominator
    print(f"{'Name':<20}{'Score':<10}{'License':<15}{'License Comp.':<15}{'Bus Factor':<15}{'Rampup':<10}{'Correctness':<15}{'Responsiveness':<15}{'Denominator':<10}")
    for pkgnames in allfinalscores.keys():
        print(f"{pkgnames:<20}{allfinalscores[pkgnames].netScore:<10}{allfinalscores[pkgnames].license:<15}{allfinalscores[pkgnames].licenseCompatibility:<15}{allfinalscores[pkgnames].busFactor:<15}{allfinalscores[pkgnames].rampUp:<10}{allfinalscores[pkgnames].correctness:<15}{allfinalscores[pkgnames].responsiveMaintainer:<15}{allfinalscores[pkgnames].denominator:<10}")


def ParseAllGitJSON(pathToGitJsonFolder, logger):
    AllGitScores = dict()
    for json in os.listdir(pathToGitJsonFolder):
        if json.endswith(".json"):
            logger.log("Parsing: " + json)
            gitjson = ImportJSON(pathToGitJsonFolder + json)
            gitscore = ParseGitJSON(gitjson)
            AllGitScores[json] = gitscore
            continue
        else:
            continue    
    return AllGitScores

def ParseAllStaticJSON(pathToStaticJsonFolder, logger):
    AllStaticScores = dict()
    for json in os.listdir(pathToStaticJsonFolder):
        if json.endswith(".json"):
            logger.log("Parsing: " + json)
            staticjson = ImportJSON(pathToStaticJsonFolder + json)
            staticscore = ParseStaticJSON(staticjson)
            AllStaticScores[json] = staticscore
            continue
        else:
            continue
    return AllStaticScores

def ParseAllNPMJSON(pathToNPMJsonFolder, logger):
    AllNPMScores = dict()
    for json in os.listdir(pathToNPMJsonFolder):
        if json.endswith(".json"):
            logger.log("Parsing: " + json)
            npmjson = ImportJSON(pathToNPMJsonFolder + json)
            npmscore = ParseNPMJSON(npmjson)
            AllNPMScores[json] = npmscore
            continue
        else:
            continue
    return AllNPMScores


def main(loglevel, logfile, DoLog=True):
    #get arguments
    Debug = logger.Logger(f"{logfile}", 2, "Grader")
    Debug.log("Log level: " + loglevel, 2)
    Debug.log("Log file: " + logfile, 2)
    
    
    #get the url string list from cache/input.txt
    durls = {}
    with open("cache/input.txt", "r") as f:
        urls = f.readlines()

        f.close()
    for url in urls:
        url = url.strip().replace("\n", "")
        #get package name cooresponding to url
        pkgname = url[url.rfind("/")+1:]
        #replace the url with the github url if it is a npm url
        
        durls[pkgname] = url

    Debug.log("URLs: " + str(durls), 2)
    
    
    #import the all files
    allnpmscores = ParseAllNPMJSON("data/npm/", Debug)
    allgitscores = ParseAllGitJSON("data/git/", Debug)
    allStaticScores = ParseAllStaticJSON("data/static/", Debug)
    
    #replace all npm urls with github urls in durls
    for pkg in durls:
        if durls[pkg].startswith("https://www.npmjs.com/package/"):
            durls[pkg] = allnpmscores[pkg + ".json"].gitrepo
            
    
    #get all durl keys as a list of strings
    packages = list(durls.keys())

    grades = dict()
    for pkg in packages:
        Debug.log("Getting score for " + pkg, 1)
        grades[pkg] = GetScore(pkg, allgitscores, allnpmscores, allStaticScores, Debug)
        Debug.log("Final score for " + pkg + ": " + str(grades[pkg].netScore), 2)
        Debug.log("Last updated: " + str(grades[pkg].lastupdated), 2)


    #prettyPrintTable(grades, "all")
    #we write it to a json format
    jsonGrades = dict()
    #{"URL":"https://github.com/nullivex/nodist", "NET_SCORE":0.9, "RAMP_UP_SCORE":0.5, "CORRECTNESS_SCORE":0.7, "BUS_FACTOR_SCORE":0.3, "RESPONSIVE_MAINTAINER_SCORE":0.4, "LICENSE_SCORE":1}
    for grade in grades:
        gradeobj = grades[grade]
        pkgname = gradeobj.name
        netscore = round(gradeobj.netScore, 1)
        rampup = round(gradeobj.rampUp / gradeobj.denominator, 1)
        correctness = round(gradeobj.correctness / gradeobj.denominator, 1)
        busfactor = round(gradeobj.busFactor / gradeobj.denominator, 1)
        responsiveMaintainer = round(gradeobj.responsiveMaintainer / gradeobj.denominator, 1)
        licenseCompatibility = gradeobj.licenseCompatibility
        jsonGrades[grade] = f"{{\"URL\":\"{durls[pkgname]}\", \"NET_SCORE\":{netscore}, \"RAMP_UP_SCORE\":{rampup}, \"CORRECTNESS_SCORE\":{correctness}, \"BUS_FACTOR_SCORE\":{busfactor}, \"RESPONSIVE_MAINTAINER_SCORE\":{responsiveMaintainer}, \"LICENSE_SCORE\":{licenseCompatibility}}}"
    
    #print the json but sorted by net score
    sortedGrades = sorted(jsonGrades, key=lambda x: grades[x].netScore, reverse=True)
    for grade in sortedGrades:
        if DoLog:
            print(jsonGrades[grade])
    

    #write the json to a file results/results.json
    with open ("results/results.ndjson", "w") as f:
        for grade in jsonGrades:
            f.writelines(jsonGrades[grade] + "\n")
        f.close()
    

    
    Debug.log("Testing Grader", 2)
    

    
    
    
if __name__ == "__main__":
    loglevel = sys.argv[1]
    logfile = sys.argv[2]
    DoLog = True
    if sys.argv[3] != '':
        DoLog = sys.argv[3]
    main(loglevel, logfile, DoLog)
    
    
    
