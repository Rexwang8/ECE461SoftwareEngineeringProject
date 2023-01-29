using System;
using System.Net;
using Newtonsoft.Json;

class Program
{
    static void Main(string[] args)
    {
        // Get the repository URL from the command-line argument
        string repoUrl = args[0];

        // Extract the owner and repository name from the URL
        string[] parts = repoUrl.Split('/');
        string owner = parts[parts.Length - 2];
        string repo = parts[parts.Length - 1];

        // Define the GraphQL query
        string query = @"
            {
              repository(owner: """ + owner + @""", name: """ + repo + @""") {
                name
                description
                stargazers {
                  totalCount
                }
              }
            }
        ";

        // Send the GraphQL query to the GitHub API
        WebClient client = new WebClient();
        string token = "YOUR_TOKEN_HERE";
        client.Headers.Add("Authorization", "Bearer " + token);
        var jsonData = new { query };
        var jsonString = JsonConvert.SerializeObject(jsonData);
        var response = client.UploadString("https://api.github.com/graphql", jsonString);
        var json = JsonConvert.DeserializeObject<dynamic>(response);

        // Print the JSON output to the console
        Console.WriteLine(json);
    }
}

