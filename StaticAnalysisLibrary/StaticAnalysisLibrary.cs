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
        public int codeCount { get; set; } //lines if code
        public int commentCount { get; set; } // lines of comments
        public int characterCount { get; set; } //code character
        public FileInfo() 
        {
            codeCount = 0; 
            commentCount = 0;
            characterCount = 0;
            //filesize, extension, readme , license, character count
        }
    }

    static public class DirectoryTool
    {
        static public string licensePath;
        static public string readmePath; 
        static public List<string> fileEntries = new List<string>();

        static public string[] jsFileExt = {".css", ".sass", ".scss", ".less", ".styl", ".html", ".htmls", ".htm", ".js", ".jsx", ".ts", ".tsx", ".cjs", ".mjs", ".iced", ".liticed", ".ls", ".es", ".es6", ".sjs", ".php", ".jsp", ".asp", ".aspx"};
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
            //Gets important files in directory path
            string[] filePaths = Directory.GetFiles(directoryPath); 
            foreach (string filePath in filePaths)
            {
                String[] splitFilePath = filePath.Split("/");
                string fileName = splitFilePath[splitFilePath.Length - 1];

                if (jsFileExt.Any(fileName.EndsWith))
                {
                    fileEntries.Add(filePath); 
                }
                else if (fileName.ToLower().Contains("license"))
                {
                    
                    licensePath = filePath;
                }
                else if (fileName.ToLower().Contains("readme"))
                {
                    readmePath = filePath;
                }
                
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
                
                //finds length of code in lines with code and comments
                String[] separator = { "//,", "/*" };
                String[] textArr = text.Split(separator, StringSplitOptions.RemoveEmptyEntries);
                fileInfo.characterCount += textArr[0].Length;
            }
            else
            {
                fileInfo.codeCount++;
                fileInfo.characterCount += text.Length;
            }


        }

        //Writes the results of Static Analysis to a file

        static public void WriteFile(string filename)
        {
            Console.WriteLine("There are " + fileInfo.codeCount + " lines of code");
            Console.WriteLine("There are " + fileInfo.commentCount + " comments");
            Console.WriteLine("There are " + fileInfo.characterCount + " code characters"); 
            Console.WriteLine("There is a license path: " + DirectoryTool.licensePath );
            Console.WriteLine("There is a license path: " + DirectoryTool.readmePath );
            

            string json = JsonSerializer.Serialize(fileInfo);
            File.WriteAllText(filename, json);
        }
    }
}
