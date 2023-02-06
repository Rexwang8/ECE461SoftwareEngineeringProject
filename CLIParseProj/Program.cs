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


            //get command line arguments


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
                //This will call the line coverage and stuff maybe? do later
            }
            else
            {
                //Test if the arg is a url
                if (Uri.IsWellFormedUriString(args[0], UriKind.Absolute))
                {
                    Console.WriteLine($"Input URI Found at  {args[0]}");
                    logger.LogToFile($"Input URI Found at {args[0]}", 1);
                    //logger.LogToFile($"/C python startup.py {args[0]} {ENVLOGLEVEL} {ENVLOGLOCATION}", ENVLOGLEVEL);
                    //startup.RunCommand($"/C python startup.py {args[0]} {ENVLOGLEVEL} {ENVLOGLOCATION}");
                }
                else
                {
                    Console.WriteLine("Invalid command, exiting...");
                    logger.LogToFile("Invalid command, exiting...", 1);
                    Environment.Exit(1);
                }
            
            }

            
            logger.LogToFile("Finished Executing C# starter script!", 1);

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
