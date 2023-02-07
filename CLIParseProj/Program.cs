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
            Console.WriteLine("Hello World!");

            //get environment variables
            int ENVLOGLEVEL = 2;
            string ENVLOGLOCATION = "log.txt";

            //get command line arguments
            bool success = int.TryParse(args[2], out ENVLOGLEVEL);
            if (!success)
            {
                if (ENVLOGLEVEL != 0)
                {
                    Console.WriteLine("Invalid log level, exiting...");
                }
                Environment.Exit(1);
            }
            ENVLOGLOCATION = args[1];

            //get current directory
            string currentDirectory = Directory.GetCurrentDirectory();

            //check if log file is absolute or relative path
            string fullPathLogger = "";

            if (System.IO.Path.IsPathRooted(ENVLOGLOCATION))
            {
                if(ENVLOGLEVEL > 1)
                {
                    Console.WriteLine("Log File Location is absolute path, using as is...");
                }
                fullPathLogger = ENVLOGLOCATION;
            }
            else
            {
                if(ENVLOGLEVEL > 1)
                {
                    Console.WriteLine(
                        "Log File Location is relative path, appending to current directory...");
                }
                fullPathLogger = currentDirectory + "\\" + ENVLOGLOCATION;
            }

            fullPathLogger = ENVLOGLOCATION;
            string command = args[0];

            if(ENVLOGLEVEL >= 1)
            {
                Console.WriteLine("Log File Location: " + fullPathLogger);
                Console.WriteLine("Log Level: " + ENVLOGLEVEL);
                Console.WriteLine("Command: " + command);
            }

            //instantiate logger
            CSharpLogger logger = new CSharpLogger(fullPathLogger, ENVLOGLEVEL);

            //Instantiate Startup Agent
            Startup startup = new Startup();

            //check if arg 0 is "install", "build", "test"
            if (args[0] == "install")
            {
                //We have already run the installation script, but we need to logg it out
                logger.Log("Installing...", 1);
                Environment.Exit(0);
            }
            else if (args[0] == "build")
            {
                logger.Log("Building...", 1);
                Environment.Exit(0);
            }
            else if (args[0] == "test")
            {
                logger.Log("Testing...", 1);
                //This will call the line coverage and stuff maybe? do later
                Environment.Exit(0);
            }
            else
            {


                logger.Log("Command: " + command, 1);


                //Test if the arg is a url
                if (!Path.IsPathRooted(command))
                {

                    logger.Log("Invalid command, exiting...", 1);
                    Environment.Exit(1);
                }
                logger.Log($"Input URI Found at {args[0]}", 1);

                //check if file exists
                if (!File.Exists(command))
                {
                    logger.Log("File does not exist, exiting...", 1);
                    Environment.Exit(1);
                }

                //check if file is a text file
                if (Path.GetExtension(command) != ".txt")
                {
                    logger.Log("File is not a text file, exiting...", 1);
                    Environment.Exit(1);
                }

                //check if file is empty
                if (new System.IO.FileInfo(command).Length == 0)
                {
                    logger.Log("File is empty, exiting...", 1);
                    Environment.Exit(1);
                }

                //Read the file at the path
                string[] lines = File.ReadAllLines(command);
                foreach (string line in lines)
                {
                    logger.Log(line, 1);
                }
                Environment.Exit(0);
            }

            logger.Log("Finished Executing C# starter script! SHOULDN't GET TO THIS POINT", 1);
            Environment.Exit(0);
        }

        //https://learn.microsoft.com/en-us/dotnet/api/system.io.path.ispathfullyqualified?view=net-7.0
        private static void ShowPathInfo(string path)
        {
            Console.WriteLine($"Path: {path}");
            Console.WriteLine($"   Rooted: {Path.IsPathRooted(path)}");
            Console.WriteLine($"   Fully qualified: {Path.IsPathFullyQualified(path)}");
            Console.WriteLine($"   Full path: {Path.GetFullPath(path)}");
            Console.WriteLine();
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
            string logLine =
                "[C# Command Parser] "
                + DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss")
                + " Priority "
                + priority.ToString()
                + " | "
                + text;
            File.AppendAllText(logFile, logLine + Environment.NewLine);
        }

        public void Log(string text, int priority)
        {
            if (!ShouldLog(this.logLevel, priority))
            {
                return;
            }

            Console.WriteLine(text);
            LogToFile(text, priority);
        }
    }
}
