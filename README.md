# ECE461SoftwareEngineeringProject
ECE 461 - Purdue Package manager for Software Engineering class.

Names: Rex Wang, Joseph Ma, Alan Zhang, Kevin Lin

A local CLI package manager project for ECE 461 - Software engineering (At purdue). Built mainly using C# and Python.


---

## General execution pattern

(C#) CLI command parser is run first. We do this because c# is compiled and we can compile an executable with it to be run indepdantly. It will be able to verify python and other dependancies is installed and run the python main script.

The main script will call all the api calls and other data parsing in order for the program to function. Execution log is saved to /log.txt

## File structure

run - shell script
Readme.md
CLIParserProj - CLI interface for shell script (C#)
startup.py - called by c# proj, calls all other scripts
...

---

## How to run program

Go to /Build and execute one of the following commands

run install - installs all dependencies including pip dependencies

run build - compiles anything that needs to be compiled

run <URL> - downloads the following URL from either npm or github and produces a NDJSON file for grades for the package.

run test - runs the static analysis test suite and exits 0 if successful

run clean - cleans all cache and log files

---

## Environment Variables

$LOG_FILE - Path to where the log file will be saved

$LOG_LEVEL - Level of logging, 0 is silent, 1 is info only, 2 is debug (everything).

$GITHUB_TOKEN - Used to access Github's graphql API
