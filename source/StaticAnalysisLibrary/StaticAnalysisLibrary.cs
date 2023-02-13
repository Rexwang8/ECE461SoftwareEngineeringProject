using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Security.Cryptography;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace StaticAnalysisLibrary
{   

    public class RepoInfo
    {
        public int codeLineCount { get; set; } //lines if code
        public int commentLineCount { get; set; } // lines of comments
        public int codeCharCount { get; set; } //code characters
        public int commentCharCount { get; set; }
        public string licensePath { get; set; }
        public string readmePath { get; set; }
        public string license {get; set; }
        public int licenseCompatibility {get; set; }
        public RepoInfo() 
        {
            codeLineCount = 0; 
            commentLineCount = 0;
            codeCharCount = 0;
            commentCharCount = 0;
            licensePath = "";
            readmePath = "";
            license = "";
            licenseCompatibility = 0;
        }
    }

    public class DirectoryTool
    {
        public List<string> sourceCodeEntries = new List<string>();
        public List<string> mdEntries = new List<string>();

        public string[] jsFileExt = {".css", ".sass", ".scss", ".less", ".styl", ".html", ".htmls", ".htm", ".js", ".jsx", ".ts", ".tsx", ".cjs", ".mjs", ".iced", ".liticed", ".ls", ".es", ".es6", ".sjs", ".php", ".jsp", ".asp", ".aspx"};
        //This function gets all the files inside dirTargetName inside directoryPath
        public void getFiles(string directoryPath, string dirTargetName, ref RepoInfo repoInfo)
        {
            try
            {
                string[] dirs = Directory.GetDirectories(directoryPath, dirTargetName, SearchOption.TopDirectoryOnly);
                string dirRoot = dirs[0];
                
                getAllFiles(dirRoot, ref repoInfo);
            }
            catch (Exception e)
            {
                Console.WriteLine("The process failed: {0}", e.ToString());
                throw;
            }
        }

        //recursive call for getFiles
        public void getAllFiles(string directoryPath, ref RepoInfo repoInfo)
        {
            //Gets important files in directory path
            string[] filePaths = Directory.GetFiles(directoryPath); 
            foreach (string filePath in filePaths)
            {
                String[] splitFilePath = filePath.Split("/");
                string fileName = splitFilePath[splitFilePath.Length - 1];

                if (jsFileExt.Any(fileName.EndsWith))
                {
                    sourceCodeEntries.Add(filePath); 
                }
                else if (fileName.ToLower().Contains("license"))
                {
                    repoInfo.licensePath = filePath;
                }
                else if (fileName.ToLower().Contains("readme"))
                {
                    repoInfo.readmePath = filePath;
                    mdEntries.Add(filePath);
                }
                else if (fileName.EndsWith(".md"))
                {
                    mdEntries.Add(filePath);
                }
                
            }

            string[] dirs = Directory.GetDirectories(directoryPath, "*", SearchOption.TopDirectoryOnly);
            foreach (string dir in dirs)
            {
                getAllFiles(dir, ref repoInfo);
            }
        }
    }

    public class StaticAnalysis
    {
        public RepoInfo repoInfo = new RepoInfo();
        DirectoryTool DirectoryTool = new DirectoryTool();

        public void Analyze(string repoBin, string targetName, string resultJsonFile)
        {
            DirectoryTool.getFiles(repoBin, targetName, ref repoInfo);
            foreach(string file in DirectoryTool.sourceCodeEntries)
            {
                ReadFile(file);
            }

            foreach(string file in DirectoryTool.mdEntries)
            {
                repoInfo.commentCharCount += File.ReadAllLines(file).Sum(s => s.Length);
            }
            LicenseParser(repoInfo.licensePath, System.IO.Directory.GetCurrentDirectory() + "/source/StaticAnalysisLibrary/LicenseList.txt", ref repoInfo);
            
            WriteFile(resultJsonFile);

            DirectoryTool.sourceCodeEntries.Clear();

        }

        //Reads the file and does the static analysis on the file
        public void ReadFile(string filename)
        {
            String? line;
           
            try
            {
                //Pass the file path and file name to the StreamReader constructor
                StreamReader sr = new StreamReader(filename);
                
                line = sr.ReadLine();
                //Continue to read until you reach end of file
                while (line != null)
                {
                    AnalyzeLine(line);
                    line = sr.ReadLine();
                }
                
                sr.Close();
            }
            catch (Exception e)
            {
                Console.WriteLine("The process failed: {0}", e.ToString());
                throw;
            }
        }

        public void AnalyzeLine(string text)
        {
            if (text.StartsWith("//") || text.StartsWith("/*"))
            {
                repoInfo.commentLineCount++;
            }
            else if (text.Contains("//") || text.Contains("/*"))
            {
                repoInfo.commentLineCount++;
                repoInfo.codeLineCount++;
                
                //finds length of code in lines with code and comments
                String[] separator = { "//,", "/*" };
                String[] textArr = text.Split(separator, StringSplitOptions.RemoveEmptyEntries);
                repoInfo.codeCharCount += textArr[0].Length;
            }
            else
            {
                repoInfo.codeLineCount++;
                repoInfo.codeCharCount += text.Length;
            }


        }

        //Writes the results of Static Analysis to a file

        public void WriteFile(string filename)
        {
            //remove file if it exists
            if (File.Exists(filename))
            {
                File.Delete(filename);
            }


            string json = JsonSerializer.Serialize(repoInfo);
            File.WriteAllText(filename, json);
        }

        
        public void LicenseParser(string LicensePath, string LicenseListPath, ref RepoInfo Repo)
        {
            if (Repo.license == "" || Repo.license == null) {
                Repo.license = "Not Available";
                return;
            }
            string License = File.ReadLines(LicensePath).First(); // gets the first line from file.
            
            var allLicenses = File.ReadAllLines(LicenseListPath);
            var allLicensesArr = new List<string>(allLicenses);
            List<string> allLicensesArrCleaned = new List<string>();
            foreach (string li in allLicensesArr)
            {
               string newli = li.Trim().ToLower();
                allLicensesArrCleaned.Add(newli);
            }



            foreach (var LicenseVar in allLicensesArrCleaned)
            {
                string cleanedlicense = License.Trim().ToLower();
                //Console.WriteLine("LicenseVar: " + LicenseVar + "|");
                string CleanedLicenseVar = LicenseVar.Trim().ToLower();
                //Console.WriteLine("Checking: " + CleanedLicenseVar + " in " + cleanedlicense + "  " + cleanedlicense.Contains(CleanedLicenseVar));
                if(cleanedlicense.Contains(CleanedLicenseVar))
                {
                    //Console.WriteLine("Found: " + CleanedLicenseVar); 
                    Repo.license = CleanedLicenseVar;
                    Repo.licenseCompatibility = 1;
                    return;
                }
            }

            Repo.license = "Not Available";
            Repo.licenseCompatibility = 0;
            return;
            
        }
    }
}
