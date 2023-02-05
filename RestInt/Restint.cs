using System.Net.Http.Headers;
namespace ConsoleProgram
{
    public class Class1
    {
        static async Task Main(string[] args)
        {
            HttpClient client = new HttpClient();
            // List data response.
            
            HttpResponseMessage response1 = await client.GetAsync("https://registry.npmjs.com/-/v1/search?text=%3Csearchstring%3E&size=20");
            HttpResponseMessage response2 = await client.GetAsync("https://api.npmjs.org/downloads/point/last-week/express");

            response1.EnsureSuccessStatusCode();
            response2.EnsureSuccessStatusCode();
            string responseBody1 = await response1.Content.ReadAsStringAsync();
            string responseBody2 = await response2.Content.ReadAsStringAsync();
            File.WriteAllText(@"C:\Users\aizha\Documents\GitHub\app\packages.json", responseBody1);
            File.WriteAllText(@"C:\Users\aizha\Documents\GitHub\app\downloads.json", responseBody2);

            // Dispose once all HttpClient calls are complete. This is not necessary if the containing object will be disposed of; for example in this case the HttpClient instance will be disposed automatically when the application terminates so the following call is superfluous.
            client.Dispose();
        }
    }
}