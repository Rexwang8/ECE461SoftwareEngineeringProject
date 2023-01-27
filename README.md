# ECE461SoftwareEngineeringProject
 ECE 461 - Purdue Package manager for Software Engineering class.

Names: Rex Wang, Joseph Ma, Alan Zhang, Kevin Lin

A local CLI package manager project for ECE 461 - Software engineering (At purdue). 


---

## General execution pattern

(C#) CLI command parser is run first. We do this because c# is compiled and we can compile an executable with it to be run indepdantly. It will be able to verify python and other dependancies is installed and run the python main script.

The main script will call all the api calls and other data parsing in order for the program to function. Execution log is saved to /log.txt

## File structure

README.md
.gitignore
.git
.gitattributes
.vs
>Command line Parser
>Command line Parser/Command line parser SLN and other files
>Build
>Build/test.py
>Build/run.exe

---

## How to build CLI Parser (C#)

1. Open .sln in visual studio
2. go to the top bar, Build > Build Solution
3. go to the folder /bin/debug/run.exe and copy it out to wherever you want to run it. Make sure it's in the same folder as the python files it's trying to run.

---


