using System.Net.Http.Headers;
namespace ConsoleProgram
{
    public class Class1
    {
        static async Task Main(string[] args)
        {
            int ENVLOGLEVEL = 2;
            string ENVLOGLOCATION = "log.txt";
            string currentDirectory = Directory.GetCurrentDirectory();
            var logpath = Path.Combine(currentDirectory, ENVLOGLOCATION);
            string command = args[0];


            CSharpLogger logger = new CSharpLogger(logpath, ENVLOGLEVEL);


            logger.Log("Command: " + command, 1);
            //Read the file at the path
            string[] lines = File.ReadAllLines(command);
            foreach (string line in lines)
            {
                logger.Log(line, 1);
            }
            Environment.Exit(0);




            logger.Log("Finished Executing C# starter script! SHOULDN't GET TO THIS POINT", 1);
            Environment.Exit(0);

            HttpClient client = new HttpClient();
            // List data response.
            string outputFile = args[0];
            string npmreg = args[1];


            int index = str.IndexOf("/package/");  
            string result = str.Substring(index, npmreg.Length);
            Console.WriteLine(result);
            
            string regURL = "https://registry.npmjs.org/" + result;
            HttpResponseMessage response1 = await client.GetAsync(regURL);

            response1.EnsureSuccessStatusCode();
            string responseBody1 = await response1.Content.ReadAsStringAsync();
            var npmpath = Path.Combine(currentDirectory, outputFile);
            File.WriteAllText(@npmpath, responseBody1);
            // Dispose once all HttpClient calls are complete. This is not necessary if the containing object will be disposed of; for example in this case the HttpClient instance will be disposed automatically when the application terminates so the following call is superfluous.
            client.Dispose();
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

                //Console.WriteLine(text);
                LogToFile(text, priority);
            }
        }
    }

}