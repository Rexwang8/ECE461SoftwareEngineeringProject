import os 
import math
import re

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
    

def formatOutput(frompy):
    #we get line cov and print to stdout
    with open ("results/lineCoverage.txt", "r") as f:
        data = f.readlines()
        f.close()

    #we get the results from csharptests

    with open("results/csharptests.txt", "r") as f:
        data2 = f.readlines()
        f.close()

    interestingstring = ""
    for i in data2:
        if "Passed:" in i:
            interestingstring = i
    is2 = interestingstring.split(', Duration')
    is3 = str(is2[0]).replace("Failed!  - ", "").replace("Pass!  - ", "")
    is4 = []
    is4 = re.findall(r'\d+', is3)
    
    failed = int(is4[0]) + (8 - int(frompy))
    passed = int(is4[1]) + int(frompy)
    total = int(is4[3]) + 8

    print(f"Total: {total}")
    print(f"Passed: {passed}")
    sdata = []
    #strip all data that is a letter or space with regex
    for aojhd in data:
        if "Total: " in aojhd:
            ashd = aojhd.replace("Total: ", "").strip()
           # print(f"Total: {ashd}")
        elif "Covered: " in aojhd:
            ahdi = float(aojhd.replace("Covered: ", "").strip())
            hiasduh = round(ahdi, 0)
            oah = int(hiasduh)
           # print(f"C: {oah}")
        elif "Coverage Percentage: ":
            kasfiu = aojhd.replace("Coverage Percentage: ", "").strip()
            hais = float(kasfiu)
            asndia = int(round(hais, -1))
            print(f"{passed}/{total} test cases passed. {asndia}% line coverage achieved.")

    

if __name__ == "__main__":
    formatOutput()