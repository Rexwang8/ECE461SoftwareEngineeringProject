using Microsoft.VisualStudio.TestTools.UnitTesting;
using StaticAnalysisLibrary;
using System.Linq;
using System;
using System.IO;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;
using System.Security.Cryptography;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace CSharpUnitTesting;


[TestClass]
public class StaticAnalysisTesting
{
    //Tests if files are retrieved correctly 
    [TestMethod]
    public void TestPassGetSourceCodeFiles()
    {
        DirectoryTool directoryTool = new DirectoryTool();
        RepoInfo repoInfo = new RepoInfo();
        
        string[] fileNames = {"cli.js", "build.js", "build.js", "github.js", "nodist.js", "npm.js", "versions.js", "npm-cli.js", "shim-node.go", "shim-npm.go", "nodist.go", "cli-test.js"};
        directoryTool.getFiles(System.IO.Directory.GetCurrentDirectory() + "/../../..", "testrepo", ref repoInfo);
        
        bool result;
        
        foreach (var filePath in directoryTool.sourceCodeEntries)
        {
            String[] splitFilePath = filePath.Split("/");
            string fileName = splitFilePath[splitFilePath.Length - 1];
            
            result = fileNames.Contains(fileName);
            Assert.IsTrue(result,
                   string.Format("Expected for '{0}': true; Actual: {1}",
                                 fileName, result));
        }
        
        result = repoInfo.licensePath.Contains("LICENSE.txt");
        Assert.IsTrue(result,
                string.Format("Expected for '{0}': true; Actual: {1}",
                                repoInfo.licensePath, result));
        
        result = repoInfo.readmePath.Contains("README.md");
        Assert.IsTrue(result,
                string.Format("Expected for '{0}': true; Actual: {1}",
                                repoInfo.licensePath, result));

        
        //System.IO.File.WriteAllLines("/home/shay/a/lin1285/ECE461SoftwareEngineeringProject/deleteMe.txt", directoryTool.sourceCodeEntries);
    }

    //Tests when dirTargetName does not exist
    [TestMethod]
    [ExpectedException(typeof(IndexOutOfRangeException), "IndexOutOfRangeException")]
    public void TestIncorrectTargetName()
    {
        DirectoryTool directoryTool = new DirectoryTool();
        RepoInfo repoInfo = new RepoInfo();    
        
        directoryTool.getFiles(System.IO.Directory.GetCurrentDirectory() + "/../../..", "testrepo2", ref repoInfo);
    }

    
    //Tests when directory path does not exist
    [TestMethod]
    [ExpectedException(typeof(IndexOutOfRangeException), "IndexOutOfRangeException")]
    public void TestIncorrectDirPath()
    {
        DirectoryTool directoryTool = new DirectoryTool();
        RepoInfo repoInfo = new RepoInfo();    
        
        directoryTool.getFiles(System.IO.Directory.GetCurrentDirectory(), "testrepo", ref repoInfo);
    }

    //Tests when dirTargetName is empty
    [TestMethod]
    [ExpectedException(typeof(ArgumentException), "ArgumentException")]
    public void TestEmptyDirPath()
    {
        StaticAnalysis staticAnalysis = new StaticAnalysis();  

        staticAnalysis.Analyze("", "testrepo",  "");
    }

    //Tests when directory path is empty
    [TestMethod]
    [ExpectedException(typeof(ArgumentException), "ArgumentException")]
    public void TestEmptyTarget()
    {
        StaticAnalysis staticAnalysis = new StaticAnalysis();  
        
        staticAnalysis.Analyze(System.IO.Directory.GetCurrentDirectory() + "/../../..", "", "");
    }

    //Tests when dirTargetName is null
    [TestMethod]
    [ExpectedException(typeof(ArgumentNullException), "ArgumentNullException")]
    public void TestNullDirPath()
    {
        StaticAnalysis staticAnalysis = new StaticAnalysis();  
        
        staticAnalysis.Analyze(null, "testrepo",  "");
    }

    //Tests when directory path is empty
    [TestMethod]
    [ExpectedException(typeof(ArgumentNullException), "ArgumentNullException")]
    public void TestNullTarget()
    {
        StaticAnalysis staticAnalysis = new StaticAnalysis();  

        staticAnalysis.Analyze(System.IO.Directory.GetCurrentDirectory() + "/../../..", null,  "");
    }

    //Tests the results of Analyze Lines
    [TestMethod]
    [ExpectedException(typeof(ArgumentException), "ArgumentException")]
    public void TestAnalyzeLine()
    {
        StaticAnalysis staticAnalysis = new StaticAnalysis();
        staticAnalysis.Analyze(System.IO.Directory.GetCurrentDirectory() + "/../../..", "testrepo",  System.IO.Directory.GetCurrentDirectory() + "/../../../testOutput"); 
    }

    //Tests when LicenseList is empty
    [TestMethod]
    [ExpectedException(typeof(ArgumentException), "ArgumentException")]
    public void TestEmptyLicensePath()
    {
        StaticAnalysis staticAnalysis = new StaticAnalysis();  

        staticAnalysis.LicenseParser("", System.IO.Directory.GetCurrentDirectory() + "/source/StaticAnalysisLibrary/LicenseList.txt",  ref staticAnalysis.repoInfo);
    }

    //Tests when LicensePath is empty
    [TestMethod]
    [ExpectedException(typeof(ArgumentException), "ArgumentException")]
    public void TestEmptyLicenseListPath()
    {
        StaticAnalysis staticAnalysis = new StaticAnalysis();  
        
        staticAnalysis.LicenseParser(staticAnalysis.repoInfo.license, "",  ref staticAnalysis.repoInfo);
    }

    [TestMethod]
    [ExpectedException(typeof(ArgumentException), "ArgumentException")]
    public void TestNullLicense()
    {
        StaticAnalysis staticAnalysis = new StaticAnalysis();
        
        staticAnalysis.LicenseParser(null, System.IO.Directory.GetCurrentDirectory() + "/source/StaticAnalysisLibrary/LicenseList.txt",  ref staticAnalysis.repoInfo);
    }

    [TestMethod]
    [ExpectedException(typeof(ArgumentException), "ArgumentException")]
    public void TestNullLicenseList()
    {
        StaticAnalysis staticAnalysis = new StaticAnalysis();
        
        staticAnalysis.LicenseParser(staticAnalysis.repoInfo.license, null,  ref staticAnalysis.repoInfo);
    }
    
}