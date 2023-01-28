using System;
using System.Diagnostics;
using System.IO;

// Hello World! program
namespace PackageManager
{
    class Startup
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello World!");

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
            }

            
            //check if arg 0 is "install", "build", "test"
            if (args[0] == "install")
            {
                Console.WriteLine("Installing...");
                //Installs any dependencies we need, including python packages
            }
            else if (args[0] == "build")
            {
                Console.WriteLine("Building...");
                //builds anything we need, I'm not sure we need anything here...
            }

            else if (args[0] == "test")
            {
                Console.WriteLine("Testing...");
                //This should launch a static analysis script
            }
            else
            {
                //Test if the arg is a url
                if (Uri.IsWellFormedUriString(args[0], UriKind.Absolute))
                {
                    Console.WriteLine($"Downloading from URL {args[0]}");
                }
                else
                {
                    Console.WriteLine("Invalid command, exiting...");
                    Environment.Exit(1);
                }
            
            }

            

            //hang the program for 1 seconds
            Console.WriteLine("Hang the program for 1 seconds");
            System.Threading.Thread.Sleep(1000);

            //instantiate class Startup
            Startup startup = new Startup();
            //startup.RunCommand("/C mkdir testdir");
            startup.LogToFile($"/C python startup.py {args[0]} {ENVLOGLEVEL} {ENVLOGLOCATION}", ENVLOGLEVEL);
            startup.RunCommand($"/C python startup.py {args[0]} {ENVLOGLEVEL} {ENVLOGLOCATION}");
            startup.LogToFile("Hello World!", ENVLOGLEVEL);


        }

        //define function for running a command
        void RunCommand(string command)
        {
            Process process = new Process();
            ProcessStartInfo startInfo = new ProcessStartInfo();
            startInfo.FileName = "cmd.exe";
            startInfo.Arguments = command;
            process.StartInfo = startInfo;
            process.Start();
        }

        //defines a function that is able to log out to log file
        /*Your software must produce a log file stored in the location named in the environment variable
         * $LOG_FILE and using the verbosity level indicated in the environment variable $LOG_LEVEL 
         * (0 means silent, 1 means informational messages, 2 means debug messages).
         * Default log verbosity is 0.*/
        void LogToFile(string text, int priority)
        {
            string logFile = "log.txt";
            string logLine = "[C# Command Parser] " + DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss") + " Priority " + priority.ToString() + " | " + text;
            File.AppendAllText(logFile, logLine + Environment.NewLine);
        }

    }



}