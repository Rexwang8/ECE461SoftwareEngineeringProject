import os 

def getCSharpResult():
    f = open(os.getcwd() + "/../../UnitTest/coverage.cobertura.xml") 
    x = f.readline()
    lineInfo = f.readline()
    for item in lineInfo.split(" "):
        if "lines-covered" in item:
            linesCovered =  int(item.split('"')[1])

        elif "lines-valid" in item:
            totalLines =  int(item.split('"')[1])

    return linesCovered, totalLines

if __name__ == "__main__":
    [linesCovered, totalLines] = getCSharpResult()
    print(linesCovered)
    print(totalLines)