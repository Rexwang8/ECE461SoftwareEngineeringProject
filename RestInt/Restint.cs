using System.Net.Http.Headers;
namespace ConsoleProgram
{
    public class Class1
    {
        static async Task Main(string[] args)
        {
            HttpClient client = new HttpClient();
            // List data response.
            
            HttpResponseMessage response = await client.GetAsync("https://registry.npmjs.com/-/v1/search?text=%3Csearchstring%3E&size=20");
            response.EnsureSuccessStatusCode();
            string responseBody = await response.Content.ReadAsStringAsync();
            File.WriteAllText(@"C:\Users\aizha\Documents\GitHub\app\fileout.json", responseBody);

            // Dispose once all HttpClient calls are complete. This is not necessary if the containing object will be disposed of; for example in this case the HttpClient instance will be disposed automatically when the application terminates so the following call is superfluous.
            client.Dispose();
        }
    }
}