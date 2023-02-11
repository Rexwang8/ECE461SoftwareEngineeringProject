using System;
using System.Diagnostics;
using System.IO;
using StaticAnalysisLibrary;
using CliWrap;
using System.Text;

// Hello World! program
namespace PackageManager
{
    class Startup
    {
        static void Main(string[] args)
        {
            //StaticAnalysis.Test();

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
            string GHTOKEN = args[3];
            

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
           /* if (args[0] == "install")
            {
                //We have already run the installation script, but we need to logg it out
                logger.LogToFile("Installing...", 1);
                Environment.Exit(0);
            }
            else if (args[0] == "build")
            {
                logger.LogToFile("Building...", 1);
                Environment.Exit(0);
            }
            else */
            if (args[0] == "test")
            {
                logger.LogToFile("Testing...", 1);
                //This will call the line coverage and stuff maybe? do later
                Environment.Exit(0);
            }
            else
            {


                logger.LogToFile("Command: " + command, 1);


                //Test if the arg is a url
                if (!Path.IsPathRooted(command))
                {

                    logger.LogToFile("Invalid command, exiting...", 1);
                    Environment.Exit(1);
                }
                logger.LogToFile($"Input URI Found at {args[0]}", 1);

                //check if file exists
                if (!File.Exists(command))
                {
                    logger.LogToFile("File does not exist, exiting...", 1);
                    Environment.Exit(1);
                }

                //check if file is a text file
                if (Path.GetExtension(command) != ".txt")
                {
                    logger.LogToFile("File is not a text file, exiting...", 1);
                    Environment.Exit(1);
                }

                //check if file is empty
                if (new System.IO.FileInfo(command).Length == 0)
                {
                    logger.LogToFile("File is empty, exiting...", 1);
                    Environment.Exit(1);
                }

                //Read the file at the path
                var stdOutBuffer = new StringBuilder();
                var stdErrBuffer = new StringBuilder();
                string[] lines = File.ReadAllLines(command);
                foreach (string line in lines)
                {
                    //wait 100ms for github api to not get rate limited
                    System.Threading.Thread.Sleep(150);

                    logger.LogToFile(line, 1);
                    //search string for either "github.com" or "npmjs.com"
                    if (line.Contains("github.com"))
                    {
                        string packageName = line.Substring(line.LastIndexOf('/') + 1);

                        //call github script
                        logger.LogToFile("Calling Github Script...", 1);

                        logger.LogToFile(packageName, 1);
                        logger.LogToFile($"command is python3 github_api/git_module.py github_api/data/" + packageName + " " + line + " " + GHTOKEN, 2);

                        var result = Cli.Wrap("python3")
                            .WithArguments($"github_api/git_module.py github_api/data/" + packageName + " " + line + " " + GHTOKEN)
                            .WithValidation(CommandResultValidation.None)
                            .WithStandardOutputPipe(PipeTarget.ToStringBuilder(stdOutBuffer))
                            .WithStandardErrorPipe(PipeTarget.ToStringBuilder(stdErrBuffer))
                            .ExecuteAsync()
                            .GetAwaiter()
                            .GetResult();

                        //Console.WriteLine("StdOut:" + stdOutBuffer.ToString());
                        //Console.WriteLine("StdErr:" + stdErrBuffer.ToString());
                    }
                    else if (line.Contains("npmjs.com"))
                    {
                        string packageName = line.Substring(line.LastIndexOf('/') + 1);
                        //call npm script
                        logger.LogToFile("Calling NPM Script...", 1);
                        
                        logger.LogToFile($"command is ./RestInt npmData " + line + " " + packageName + " " + ENVLOGLEVEL + " " + ENVLOGLOCATION, 2);
                        var result = Cli.Wrap("./RestInt")
                            .WithArguments($"npmData " + line + " " + packageName + " " + ENVLOGLEVEL + " " + ENVLOGLOCATION)
                            .WithValidation(CommandResultValidation.None)
                            .WithStandardOutputPipe(PipeTarget.ToStringBuilder(stdOutBuffer))
                            .WithStandardErrorPipe(PipeTarget.ToStringBuilder(stdErrBuffer))
                            .ExecuteAsync()
                            .GetAwaiter()
                            .GetResult();
                        
                        //Console.WriteLine("StdOut:" + stdOutBuffer.ToString());
                        //Console.WriteLine("StdErr:" + stdErrBuffer.ToString());
                        //startup.NpmScript(line);
                    }
                    else
                    {
                        logger.LogToFile("Invalid URI, exiting...", 1);
                        Environment.Exit(1);
                    }
                    
                
                }
                //At this point, we have the metadata for all the packages, we need to call the python script for grading
                logger.LogToFile("Calling Python Script...", 1);
                var result = Cli.Wrap("python3")
                            .WithArguments($"startup.py")
                            .WithValidation(CommandResultValidation.None)
                            .WithStandardOutputPipe(PipeTarget.ToStringBuilder(stdOutBuffer))
                            .WithStandardErrorPipe(PipeTarget.ToStringBuilder(stdErrBuffer))
                            .ExecuteAsync()
                            .GetAwaiter()
                            .GetResult();
                Environment.Exit(0);
            }

            logger.LogToFile("Finished Executing C# starter script! SHOULDN't GET TO THIS POINT", 1);
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
                "[C# NPM Grabber] "
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
