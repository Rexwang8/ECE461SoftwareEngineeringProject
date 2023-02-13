#run this file by using pytest unittest.py

def git_module1(url):
    from github_api import git_module
    return git_module.parse_github_url("https://github.com/Rexwang8/ECE461SoftwareEngineeringProject")[0]

def git_module2(url):
    from github_api import git_module
    return git_module.parse_github_url("https://github.com/Rexwang8/ECE461SoftwareEngineeringProject")[1]

def logger_setpriority(x):
    import logger
    mylog = logger.Logger()
    mylog.setpriority(x)
    return mylog.internalpriority

def logger_setpath(path):
    import logger
    mylog = logger.Logger()
    mylog.setpath(path)
    return mylog.path

def logger_scriptname(name):
    import logger
    mylog = logger.Logger()
    mylog.setscriptname(name)
    return mylog.scriptname

def grader_score_busfactor():
    import grader
    score = grader.Score()
    return score.busFactor

def grader_score_rampup():
    import grader
    score = grader.Score()
    return score.rampUp

def grader_score_license():
    import grader
    score = grader.Score()
    return score.license

def test_module():
    return git_module1("https://github.com/Rexwang8/ECE461SoftwareEngineeringProject") == "Rexwang8" 
    
def test_module2():
    return git_module2("https://github.com/Rexwang8/ECE461SoftwareEngineeringProject") == "ECE461SoftwareEngineeringProject"  

def test_logger_priority():
    return logger_setpriority(1) == 1

def test_logger_path():
    return logger_setpath("mypath") == "mypath"

def test_logger_script():
    return logger_scriptname("script") == "script"

def test_score_busfactor():
    return grader_score_busfactor() == 0

def test_score_rampup():
    return grader_score_rampup() == 0

def test_score_license():
    return grader_score_license() == 'MIT'

def testAll():
    total = 0
    total += test_module()
    total += test_module2()
    total += test_logger_priority()
    total += test_logger_path()
    total += test_logger_script()
    total += test_score_busfactor()
    total += test_score_rampup()
    total += test_score_license()
    #print("Total test cases passed: " + str(total) + "/8")
    return total


