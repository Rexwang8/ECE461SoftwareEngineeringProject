using StaticAnalysisLibrary;
using CliWrap;
using System.Text;

namespace StaticTest
{
    class ClassStaticTest
    {
        static void Main(string[] args)
        {
//get arg1 as log level in int and arg2 as log file path
int loglevel = int.Parse(args[0]);
string logpath = args[1];
CSharpLogger logger = new CSharpLogger(logpath, loglevel);

logger.LogToFile("Log File Location: " + logpath, 1);
logger.LogToFile("Log Level: " + loglevel, 1);

//instantiate static analysis
StaticAnalysis StaticAnalysis = new StaticAnalysis();
string currentDirectory = Directory.GetCurrentDirectory();
string pathToRepoFolder = Path.Combine(currentDirectory, "data", "repo");

//for each folder in the repo folder
for (int i = 0; i < Directory.GetDirectories(pathToRepoFolder).Length; i++)
{
    //get the name of the folder
    string folderName = Path.GetFileName(Directory.GetDirectories(pathToRepoFolder)[i]);
    //get the path to the folder
    string pathToFolder = Path.Combine(pathToRepoFolder, folderName);

    //We save results to data/static/
    string pathToResultsFolder = Path.Combine(currentDirectory, "data", "static");
    //get the path to the json file
    string pathToJson = Path.Combine(pathToResultsFolder, folderName + ".json");

    logger.LogToFile("Analyzing folder " + folderName, 1);
    //Console.WriteLine("Analyzing folder " + folderName);
    logger.LogToFile("Saving results to " + pathToJson, 1);
    //analyze the folder
    StaticAnalysis.Analyze(pathToRepoFolder, folderName, pathToJson);
}

logger.LogToFile("Done with static analysis", 1);
logger.LogToFile("Calling grader.py", 1);
logger.LogToFile("Log File Location: " + logpath, 1);
logger.LogToFile("Log Level: " + loglevel, 1);

//We are now done with static analysis, we call grader to parse the results
var stdOutBuffer = new StringBuilder();
var stdErrBuffer = new StringBuilder();
var results = Cli.Wrap("python3")
    .WithArguments("source/pyscripts/grader.py " + loglevel + " " + logpath + " true")
    .WithValidation(CommandResultValidation.None)
    .WithStandardOutputPipe(PipeTarget.ToStringBuilder(stdOutBuffer))
    .WithStandardErrorPipe(PipeTarget.ToStringBuilder(stdErrBuffer))
    .ExecuteAsync()
    .GetAwaiter()
    .GetResult();

string buffer = stdOutBuffer.ToString();
Console.WriteLine(buffer);



//log the results
logger.LogToFile(stdOutBuffer.ToString(), 2);
logger.LogToFile(stdErrBuffer.ToString(), 2);
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

            string logLine =
                "[C# Static Analysis Caller (source/StaticAnalysisTesterProj/Program2.cs)] "
                + DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss")
                + " Priority "
                + priority.ToString()
                + " | "
                + text;
            File.AppendAllText(logFile, logLine + Environment.NewLine);
        }

    }
}


