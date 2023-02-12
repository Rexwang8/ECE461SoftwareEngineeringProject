using System.Net.Http.Headers;
namespace ConsoleProgram
{
    public class Class1
    {
        static async Task Main(string[] args)
        {
            HttpClient client = new HttpClient();
            // List data response.
            string npmreg = args[1];
            string packageName = args[2];
            int ENVLOGLEVEL = 2;
            bool success = int.TryParse(args[3], out ENVLOGLEVEL);
            if (!success)
            {
                Environment.Exit(1);
            }

            string ENVLOGLOCATION = args[4];
            //get current directory
            string currentDirectory = Directory.GetCurrentDirectory();

            //check if log file is absolute or relative path
            string fullPathLogger = "";

            if (System.IO.Path.IsPathRooted(ENVLOGLOCATION) == true)
            {
                fullPathLogger = ENVLOGLOCATION;
            }
            else
            {
                fullPathLogger = currentDirectory + "\\" + ENVLOGLOCATION;
            }

            fullPathLogger = ENVLOGLOCATION;

            CSharpLogger logger = new CSharpLogger(fullPathLogger, ENVLOGLEVEL);


            
            string regURL = "https://registry.npmjs.org/" + packageName;
            Console.WriteLine("URL: " + regURL);
            HttpResponseMessage response = await client.GetAsync(regURL);

            if(response.IsSuccessStatusCode)
            {
                logger.LogToFile("Response from registry.npmjs.org: " + response.StatusCode, 1);
            }
            else
            {
                logger.LogToFile("Response from registry.npmjs.org: " + response.StatusCode, 1);
                Environment.Exit(1);
            }

            string responseBody = await response.Content.ReadAsStringAsync();
            var npmpath = Path.Combine(currentDirectory, "data/npm/" + packageName + ".json");
            Console.WriteLine("Writing to file: " + npmpath);

            //make file if it doesn't exist
            if (!File.Exists(npmpath))
            {
                File.Create(npmpath);
            }

            File.WriteAllText(@npmpath, responseBody);
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

                string logLine =
                    "[C# NPM Grbber] "
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

                LogToFile(text, priority);
            }
        }
    }

}