using System;
using System.Net.Http;
using Newtonsoft.Json;

class Program
{
    static async Task Main(string[] args)
    {
        // Parse the URL from the command-line argument
        var url = args[0];

        // Create an HttpClient
        var httpClient = new HttpClient();

        // Set the headers for the request
        httpClient.DefaultRequestHeaders.Accept.Add(
            new System.Net.Http.Headers.MediaTypeWithQualityHeaderValue("application/json"));
        httpClient.DefaultRequestHeaders.Add("User-Agent", "C# App");

        // Create the GraphQL query
        var query = @"
        {
            repository(owner: ""OWNER"", name: ""REPO"") {
                name
                description
                createdAt
                pushedAt
                stargazers {
                    totalCount
                }
                issues {
                    totalCount
                }
            }
        }
        ";

        // Replace the placeholders in the query with the values from the URL
        query = query.Replace("OWNER", "OWNER").Replace("REPO", "REPO");

        // Create a request object
        var request = new
        {
            query = query
        };

        // Serialize the request object to a JSON string
        var json = JsonConvert.SerializeObject(request);

        // Create a StringContent object with the JSON string and the appropriate content type
        var stringContent = new StringContent(json, Encoding.UTF8, "application/json");

        // Make the GraphQL API call and get the response
        var response = await httpClient.PostAsync(url, stringContent);

        // Read the response as a string
        var responseString = await response.Content.ReadAsStringAsync();

        // Deserialize the response string to a JSON object
        var jsonResponse = JsonConvert.DeserializeObject(responseString);

        // Write the JSON object to the console
        Console.WriteLine(jsonResponse);
    }
}
