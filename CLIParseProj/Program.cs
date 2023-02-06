using System;
using System.Diagnostics;
using System.IO;
using StaticAnalysisLibrary;

// Hello World! program
namespace PackageManager
{
    class Startup
    {
        static void Main(string[] args)
        {
            
            StaticAnalysis.Test();
            
            //get environment variables
            int ENVLOGLEVEL = 2;
            string ENVLOGLOCATION = "log.txt";

            //KEEP THIS COMMENTED -------------- FOR DEBUGGING
            /*
            bool result = Int32.TryParse(Environment.GetEnvironmentVariable("$LOG_LEVEL"), out ENVLOGLEVEL);

            if (!result)
            {
                Console.WriteLine("Error: Environment variable $LOG_LEVEL is not set or set properly");
                Environment.Exit(1);
            }

            
            //ENVLOGLOCATION = Environment.GetEnvironmentVariable("$LOG_FILE");
            */


            //get command line arguments
            /*
            if (args.Length > 0)
            {
                if (ENVLOGLEVEL > 1)
                {
                    Console.WriteLine("Command line arguments:");
                    foreach (string arg in args)
                    {
                        Console.WriteLine(arg);
                    }
                }
            }*/

            ENVLOGLEVEL = int.Parse(args[1]);
            ENVLOGLOCATION = args[2];

            //get current directory
            string currentDirectory = Directory.GetCurrentDirectory();

            //check if log file is absolute or relative path
            string fullPathLogger = "";
            if (System.IO.Path.IsPathRooted(ENVLOGLOCATION))
            {
                fullPathLogger = ENVLOGLOCATION;
            }
            else
            {
                fullPathLogger = currentDirectory + "\\" + ENVLOGLOCATION;
            }

            //instantiate logger
            CSharpLogger logger = new CSharpLogger(fullPathLogger, ENVLOGLEVEL);

            //Instantiate Startup Agent
            Startup startup = new Startup();

            //check if arg 0 is "install", "build", "test"
            if (args[0] == "install")
            {
                //We have already run the installation script, but we need to logg it out
                Console.WriteLine("Logging Installation to file...");
                logger.LogToFile("Logging Installation to file...", 1);

                //We take the results from the /cache/pip.txt file and log it to the log file
                string pipinstall = File.ReadAllText("cache/pip.txt");
                logger.LogToFile(pipinstall, 2);

            }
            else if (args[0] == "build")
            {
                Console.WriteLine("Building...");
                logger.LogToFile("Building...", 1);

                //We take the results from the /cache/build.txt file and log it to the log file
                string build = File.ReadAllText("cache/build.txt");
                logger.LogToFile(build, 2);
            }

            else if (args[0] == "test")
            {
                Console.WriteLine("Testing...");
                logger.LogToFile("Testing...", 1);
                //logger.LogToFile($"/C python startup.py {args[0]} {ENVLOGLEVEL} {ENVLOGLOCATION}", ENVLOGLEVEL);
                //startup.RunCommand($"/C python startup.py {args[0]} {ENVLOGLEVEL} {ENVLOGLOCATION}");
                //This should launch a static analysis script
            }
            else
            {
                //Test if the arg is a url
                if (Uri.IsWellFormedUriString(args[0], UriKind.Absolute))
                {
                    Console.WriteLine($"Downloading from URL {args[0]}");
                    logger.LogToFile($"Downloading from URL {args[0]}", 1);
                    logger.LogToFile($"/C python startup.py {args[0]} {ENVLOGLEVEL} {ENVLOGLOCATION}", ENVLOGLEVEL);
                    startup.RunCommand($"/C python startup.py {args[0]} {ENVLOGLEVEL} {ENVLOGLOCATION}");
                }
                else
                {
                    Console.WriteLine("Invalid command, exiting...");
                    logger.LogToFile("Invalid command, exiting...", 1);
                    //logger.LogToFile($"/C python startup.py {args[0]} {ENVLOGLEVEL} {ENVLOGLOCATION}", ENVLOGLEVEL);
                    //startup.RunCommand($"/C python startup.py {args[0]} {ENVLOGLEVEL} {ENVLOGLOCATION}");
                    Environment.Exit(1);
                }
            
            }

            
            logger.LogToFile("Finished Executing C# starter script!", 1);

        }




        //define function for running a command #DEPRECATED, ONLY FOR TESTING
        string RunCommand(string command)
        {
            Process process = new Process();
            ProcessStartInfo startInfo = new ProcessStartInfo();
            startInfo.FileName = "cmd.exe";
            startInfo.Arguments = command;
            process.StartInfo = startInfo;
            startInfo.UseShellExecute = false;
            
            startInfo.RedirectStandardOutput = true;
            process.Start();
            string output = process.StandardOutput.ReadToEnd();
            process.WaitForExit();
            return output;
        }


        //Runs pip install requirements if needed, HANDLED BY SHELL SCRIPT NOW
        void Install(Startup startup, CSharpLogger logger)
        {
            //check if python is installed
            string pythonversion = startup.RunCommand("/C python --version");
            logger.LogToFile(pythonversion, 1);
            //check if pip is installed
            string pipversion = startup.RunCommand("/C pip --version");
            logger.LogToFile(pipversion, 2);

            //install requirements
            string pipinstall = startup.RunCommand("/C pip install -r requirements.txt");
            logger.LogToFile(pipinstall, 2);


            //WE DO NOT NEED TO INSTALL DOTNET PACKAGES BECAUSE THEY ARE COMPILED
            //install dotnet package newtonsoft.json
            //string dotnetinstall = startup.RunCommand("/C dotnet add package Newtonsoft.Json");
            //logger.LogToFile(dotnetinstall, 2);
        }

        void Build(Startup startup, CSharpLogger logger) //HANDLED BY SHELL SCRIPT NOW
        {
            //builds anything we need, I'm not sure we need anything here...
            startup.Install(startup, logger);
        }

    }


    public class CSharpLogger
    {
        //declare variables
        private string logFile;
        private int logLevel;

        public CSharpLogger(string logFile, int logLevel)
        {
            //Initialize Logger
            this.logFile = logFile; //Absolute path
            this.logLevel = logLevel; //0 for silent, 1 for info, 2 for info and debug
        }

        //predicate to decide if you should log
        bool ShouldLog(int priority, int messagePriority)
        {
            if (priority == 0 || messagePriority == 0)
            {
                return false;
            }

            //should return false for p=1 and m=2, true for all other cases
            if (priority >= messagePriority)
            {
                return true;
            }
            else
            {
                return false;
            }

        }

        //defines a function that is able to log out to log file
        /*Your software must produce a log file stored in the location named in the environment variable
         * $LOG_FILE and using the verbosity level indicated in the environment variable $LOG_LEVEL 
         * (0 means silent, 1 means informational messages, 2 means debug messages).
         * Default log verbosity is 0.*/
        public void LogToFile(string text, int priority)
        {
            if (!ShouldLog(this.logLevel, priority))
            {
                return;
            }

            //string logFile = "log.txt";
            string logLine = "[C# Command Parser] " + DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss") + " Priority " + priority.ToString() + " | " + text;
            File.AppendAllText(logFile, logLine + Environment.NewLine);
        }
    }
}
