import coverage
import os
import sys
cov = coverage.Coverage(source=['grader', 'gitPython','github_api', 'logger'])
cov.start()

LOG_PATH = "/Users/Josephma/461_project/source/pyscripts/test.txt"
LOG_FILE = "/Users/Josephma/461project2/testcache2"

#sys.argv[1] is LOG_FILE
#sys.argv[2] is LOG_LEVEL
#sys.argv[3] is GITHUB_TOKEN

LOG_FILE = sys.argv[1]
LOG_PATH = sys.argv[2]
GHTOKEN = sys.argv[3]

###########################
#Testing logger.py
##########################
import logger as l
from github_api import git_module as module
#create 10 tests
log = [0] * 3
for i in range(3):
        log[i] = l.Logger()
        log[i].setpriority(2 - i)
        log[i].setscriptname("log" + str(i))
        log[i].setpath("cache/path" + str(i))
        log[i].setscriptname("test_directory")
        log[i].log("the message", i)

log_test = l.Logger()
log_test.setpriority(1)
log_test.setscriptname("log_test")
log_test.setpath("cache")
log_test.setscriptname("scriptname")
log_test.log("msg", 2)

log_test2 = l.Logger()
log_test2.setpriority(2)
log_test2.setscriptname("log_test")
log_test2.setpath("cache/pathX")
log_test2.setscriptname("scriptname")
log_test2.log("msg", 1)

log_test3 = l.Logger()
log_test3.setpriority(2)
log_test3.setscriptname("log_test")
log_test3.setpath("cache/pathY")
log_test3.setscriptname("scriptname")
log_test3.log("msg", 2)

log_test2 = l.Logger()
log_test2.setpriority(0)
log_test2.setscriptname("log_test")
log_test2.setpath("cache/pathZ")
log_test2.setscriptname("scriptname")
log_test2.log("msg", 1)

###########################
#Testing git_module.py
##########################

#we're calling from line_coverage.py just to test line coverage
the_url = "https://github.com/Rexwang8/ECE461SoftwareEngineeringProject" #put in testing parameters
the_name = "cache/myfile"
module.run_git_module(the_name, the_url, GHTOKEN)

###########################
#Testing gitPython.py
##########################
import gitPython
gitPython.pythonGit.pyClone("invalidURL","invalidPath")

###########################
#Testing grader.py 
##########################

import grader as grade
grade.main(LOG_PATH, LOG_FILE)

#save the coverage tests
cov.stop()
cov.save()
cov.load()

percent = cov.report()
print(str(percent) + "%")
