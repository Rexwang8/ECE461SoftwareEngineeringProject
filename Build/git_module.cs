using System;
using System.IO;
using System.Net.Http;
using Newtonsoft.Json;

class Program
{
	static void Main(string[] args)
	{
		var url = args[0] //url of repository passed as command line argument
		
		//Define the GraphQL query
		var query = "{ repository(url: \"" + url + "\") { name description createdAt stargazers { totalCount } issues { totalCount } pullRequests { totalCount } } }";
		
		// Create a new instance of HttpClient
		using (var client = new HttpClient())
		{
			//authorization header
			client.DefaultRequestHeaders.Add("Authorization", "Bearer YOUR_TOKEN_HERE");

			//Create a new instance of StringContent
			var content = new StringContent(JsonConvert.SerializeObject(new { query }), System.Text.Encoding.UTF8, "application/json");

			//Make API call
			var response = client.PostAsync("https://api.github.com/graphql", content).Result;

			//Read the JSON output
			var json = response.Content.ReadAsStringAsync().Result();

			//write JSON output to a file
			File.WriteAllText("output.json", json);
		}
	}
}
