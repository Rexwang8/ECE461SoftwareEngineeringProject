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
        public int lineCount { get; set; }
        public int commentCount { get; set; }
        public FileInfo() 
        {
            lineCount = 0; 
            commentCount = 0;
        }
    }
    static public class StaticAnalysis
    {
        static FileInfo fileInfo = new FileInfo();

        static public void Test()
        {
            Console.WriteLine("FUCK");
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
            finally
            {
                Console.WriteLine("Executing finally block.");
            }

        }

        //
        static public void AnalyzeLine(string text)
        {
            fileInfo.lineCount++;

            if (text.Contains("//"))
            {
                fileInfo.commentCount++;
            }


        }

        //Writes the results of Static Analysis to a file

        static public void WriteFile(string filename)
        {
            Console.WriteLine("There are " + fileInfo.lineCount + " lines");
            Console.WriteLine("There are " + fileInfo.commentCount + " comments");

            // need to create a list of data for each file inside the library 

            string json = JsonSerializer.Serialize(fileInfo);
            File.WriteAllText(filename, json);
        }
    }
}
