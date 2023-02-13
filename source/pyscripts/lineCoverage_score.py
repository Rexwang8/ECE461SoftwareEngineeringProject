import os 
import logger

def getCSharpResult():
    f = open("UnitTest/coverage.cobertura.xml") 
    x = f.readline()
    lineInfo = f.readline()
    for item in lineInfo.split(" "):
        if "lines-covered" in item:
            linesCovered =  int(item.split('"')[1])

        elif "lines-valid" in item:
            totalLines =  int(item.split('"')[1])

    return linesCovered, totalLines

if __name__ == "__main__":
    [linesCovered_cSharp, totalLines_cSharp] = getCSharpResult()
    
    linesCovered = linesCovered_cSharp
    totalLines = totalLines_cSharp

    
    logObject = logger.Logger(path="results", name="lineCoverage.txt")
    logObject.log(msg="Total: " + str(totalLines))
    print("Total: " + str(totalLines))
    logObject.log(msg="Covered: " + str(linesCovered))
    print("Covered: " + str(linesCovered))
    logObject.log(msg="Coverage Percentage: " + str(linesCovered/totalLines))
    print("Coverage Percentage: " + str(linesCovered/totalLines * 100))