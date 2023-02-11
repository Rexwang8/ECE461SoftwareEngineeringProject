// See https://aka.ms/new-console-template for more information
using StaticAnalysisLibrary;

StaticAnalysis StaticAnalysis = new StaticAnalysis();
string currentDirectory = Directory.GetCurrentDirectory();
string pathToRepoFolder = Path.Combine(currentDirectory, "repo");

//for each folder in the repo folder
for (int i = 0; i < Directory.GetDirectories(pathToRepoFolder).Length; i++)
{
    //get the name of the folder
    string folderName = Path.GetFileName(Directory.GetDirectories(pathToRepoFolder)[i]);
    //get the path to the folder
    string pathToFolder = Path.Combine(pathToRepoFolder, folderName);

    //We save results to results/static/
    string pathToResultsFolder = Path.Combine(currentDirectory, "results", "static");
    //get the path to the json file
    string pathToJson = Path.Combine(pathToResultsFolder, folderName + ".json");

    //analyze the folder
    StaticAnalysis.Analyze(pathToFolder, folderName, pathToJson);
}

//StaticAnalysis.Analyze("/home/shay/a/lin1285/ECE461SoftwareEngineeringProject/testRepo", "dog", "/home/shay/a/lin1285/ECE461SoftwareEngineeringProject/test.json");
//Console.WriteLine("Hello, World!");
