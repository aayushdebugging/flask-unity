using System;
using System.Net.Http;
using System.Threading;
using System.Threading.Tasks;
using Newtonsoft.Json;

class Program
{
    static async Task Main(string[] args)
    {
        string apiUrl = "http://127.0.0.1:5000/api/update";  // Replace with your Flask API endpoint

        using (var client = new HttpClient())
        {
            while (true)
            {
                try
                {
                    // Fetch data from Flask API
                    var response = await client.GetAsync(apiUrl);

                    if (response.IsSuccessStatusCode)
                    {
                        var jsonString = await response.Content.ReadAsStringAsync();
                        var jsonData = JsonConvert.DeserializeObject<dynamic>(jsonString);

                        // Access and use the JSON data
                        double size = jsonData.size;
                        string color = jsonData.color;

                        // Print size and color values
                        Console.WriteLine($"Size: {size}");
                        Console.WriteLine($"Color: {color}");
                    }
                    else
                    {
                        Console.WriteLine($"Failed to fetch data: {response.StatusCode}");
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Error: {ex.Message}");
                }

                // Adjust the delay based on your update frequency from Flask
                Thread.Sleep(1000);  // Poll every second
            }
        }
    }
}
