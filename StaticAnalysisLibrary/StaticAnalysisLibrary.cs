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
    public class FileInfo
    {
        public int codeCount { get; set; }
        public int commentCount { get; set; }
        public FileInfo() 
        {
            codeCount = 0; 
            commentCount = 0;
        }
    }

    static public class DirectoryTool
    {

        static public List<string> fileEntries = new List<string>();

        //This function gets all the files inside dirTargetName inside directoryPath
        static public void getFiles(string directoryPath, string dirTargetName)
        {
            try
            {
                string[] dirs = Directory.GetDirectories(directoryPath, dirTargetName, SearchOption.TopDirectoryOnly);
                string dirRoot = dirs[0];
                
                getAllFiles(dirRoot);
            }
            catch (Exception e)
            {
                Console.WriteLine("The process failed: {0}", e.ToString());
            }
        }

        //recursive call for getFiles
        static public void getAllFiles(string directoryPath)
        {
            //Gets all files in directory path
            string[] fileNames = Directory.GetFiles(directoryPath); 
            foreach (string fileName in fileNames)
            {
                
                fileEntries.Add(fileName); 
            }

            string[] dirs = Directory.GetDirectories(directoryPath, "*", SearchOption.TopDirectoryOnly);
            foreach (string dir in dirs)
            {
                getAllFiles(dir);
            }
        }
    }

    static public class StaticAnalysis
    {
        static FileInfo fileInfo = new FileInfo();

        static public void Analyze(string repoBin, string targetName, string resultJsonFile)
        {
            DirectoryTool.getFiles(repoBin, targetName);
            foreach(string file in DirectoryTool.fileEntries)
            {
                ReadFile(file);
            }
            
            WriteFile(resultJsonFile);

            DirectoryTool.fileEntries.Clear();
        }

        //Reads the file and does the static analysis on the file
        static public void ReadFile(string filename)
        {
            String line;
           
            try
            {
                //Pass the file path and file name to the StreamReader constructor
                StreamReader sr = new StreamReader(filename);
                //Read the first line of text
                line = sr.ReadLine();
                //Continue to read until you reach end of file
                while (line != null)
                {
                    //Console.WriteLine(line);
                    AnalyzeLine(line);
                    //Read the next line
                    line = sr.ReadLine();
                    
                }
                //close the file
                sr.Close();
            }
            catch (Exception e)
            {
                Console.WriteLine("Exception: " + e.Message);
            }
        }

        //
        static public void AnalyzeLine(string text)
        {
            if (text.StartsWith("//") || text.StartsWith("/*"))
            {
                fileInfo.commentCount++;
            }
            else if (text.Contains("//") || text.Contains("/*"))
            {
                fileInfo.commentCount++;
                fileInfo.codeCount++;
            }
            else
            {
                fileInfo.codeCount++;
            }


        }

        //Writes the results of Static Analysis to a file

        static public void WriteFile(string filename)
        {
            Console.WriteLine("There are " + fileInfo.codeCount + " lines of code");
            Console.WriteLine("There are " + fileInfo.commentCount + " comments");

            // need to create a list of data for each file inside the library 

            string json = JsonSerializer.Serialize(fileInfo);
            File.WriteAllText(filename, json);
        }
    }
}
