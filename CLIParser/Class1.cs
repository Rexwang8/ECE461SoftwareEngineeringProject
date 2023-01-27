using System;
using System.Diagnostics;
using System.IO;

// Hello World! program
namespace HelloWorld
{
    class Hello
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello World!");
            int LogLevel = 0;

            //get command line arguments
            if (args.Length > 0)
            {
                Console.WriteLine("Command line arguments are:");
                for (int i = 0; i < args.Length; i++)
                {
                    Console.WriteLine(args[i]);
                }
            }

            //hang the program for 1 seconds
            Console.WriteLine("Hang the program for 1 seconds");
            System.Threading.Thread.Sleep(1000);

            //instantiate class Hello
            Hello hello = new Hello();
            hello.RunCommand("/C mkdir testdir");
            hello.RunCommand("/C python test.py arg1 arg2 arg3 blah blah blah");
            hello.LogToFile("Hello World!", LogLevel);



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