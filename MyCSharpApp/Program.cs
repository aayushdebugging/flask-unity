using System;
using System.Net.Http;
using System.Threading;
using System.Threading.Tasks;
using Newtonsoft.Json;
using System.IO;
using Newtonsoft.Json.Linq;

class Program
{
    static async Task Main(string[] args)
    {
        string apiUrl = "http://127.0.0.1:5000/api/update";  // Replace with your Flask API endpoint
        string localDataFilePath = "../data.json"; // Path to data.json outside MyCSharpApp directory

        using (var client = new HttpClient())
        {
            while (true)
            {
                try
                {
                    var response = await client.GetAsync(apiUrl);

                    if (response.IsSuccessStatusCode)
                    {
                        var jsonString = await response.Content.ReadAsStringAsync();
                        var jsonData = JsonConvert.DeserializeObject<dynamic>(jsonString);

                        foreach (var item in jsonData)
                        {
                            string key = item.Name;
                            var value = item.Value;

                            double longitude = value.longitude;
                            double latitude = value.latitude;
                            double size = value.size;
                            string color = value.color;

                            // Print variable name, longitude, latitude, size, and color values
                            Console.WriteLine($"{key}: Longitude: {longitude}, Latitude: {latitude}, Size: {size}, Color: {color}");
                        }

                        // Write the data to data.json
                        File.WriteAllText(localDataFilePath, jsonString.ToString());
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

                Thread.Sleep(1000);  // Poll every second
            }
        }
    }
}
