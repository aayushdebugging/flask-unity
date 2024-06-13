
# Flask-CSharp Integration Project

## Project Description

This project demonstrates how to create a simple integration between a Python Flask application and a C# console application. The Flask application continuously generates simulated data, including oxygen levels, pollutant levels, size, and color. The C# application fetches this data via an HTTP API, displays it in the console, and stores it locally in a JSON file.

## Project Structure

```
project/
│
├── FlaskApp/                # Contains the Flask application code
│   ├── app.py               # Main Flask application file
│   └── requirements.txt     # Python dependencies
│
├── MyCSharpApp/             # Contains the C# console application code
│   └── Program.cs           # Main C# application file
│
├── data.json                # Local storage for fetched data, located outside of MyCSharpApp
│
└── README.md                # Project README file
```

## Prerequisites

- Python 3.x
- .NET Core SDK
- Visual Studio Code or another suitable IDE
- Git

## Setup Instructions

### Setting Up the Flask Application

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/Flask-CSharp-Integration.git
    cd Flask-CSharp-Integration/FlaskApp
    ```

2. **Create a virtual environment**:

    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment**:

    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

5. **Run the Flask application**:

    ```bash
    python app.py
    ```

    The Flask application will start running at `http://127.0.0.1:5000`.

### Setting Up the C# Application

1. **Navigate to the C# project directory**:

    ```bash
    cd ../MyCSharpApp
    ```

2. **Ensure the `data.json` file exists**:

    Create a `data.json` file outside the `MyCSharpApp` directory. This file will be used to store the fetched data from the Flask API.

    ```bash
    echo "{}" > ../data.json
    ```

3. **Build and run the C# application**:

    ```bash
    dotnet run
    ```

    The C# application will start fetching data from the Flask API, printing the values to the console, and storing the latest data in `../data.json`.

## Usage

1. **Run the Flask application**:

    Start the Flask server to generate and serve the data.

2. **Run the C# application**:

    Execute the C# application to fetch and display the data from the Flask API. The `size` and `color` values will be printed in the console and the data will be continuously updated in `../data.json`.

### Flask Application Code (`app.py`)

```python
from flask import Flask, jsonify
import time
import random

app = Flask(__name__)

def generate_data():
    while True:
        oxygen_level = random.randint(0, 100)
        pollutant_level = random.randint(0, 100)

        red = min(255, int(255 * (100 - oxygen_level) / 100))
        green = min(255, int(255 * oxygen_level / 100))
        blue = 0
        color = f"rgb({red}, {green}, {blue})"

        size = 0.1 + (pollutant_level / 100) * 0.9

        data = {
            'oxygen_level': oxygen_level,
            'pollutant_level': pollutant_level,
            'size': size,
            'color': color
        }

        yield jsonify(data)
        time.sleep(1)

@app.route('/api/update', methods=['GET'])
def update_data():
    return next(generate_data())

if __name__ == "__main__":
    app.run(debug=True)
```

### C# Application Code (`Program.cs`)

```csharp
using System;
using System.Net.Http;
using System.Threading;
using System.Threading.Tasks;
using Newtonsoft.Json;
using System.IO;

class Program
{
    static async Task Main(string[] args)
    {
        string apiUrl = "http://127.0.0.1:5000/api/update";  
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

                        double size = jsonData.size;
                        string color = jsonData.color;

                        Console.WriteLine($"Size: {size}");
                        Console.WriteLine($"Color: {color}");

                        File.WriteAllText(localDataFilePath, jsonString);
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

                Thread.Sleep(1000);  
            }
        }
    }
}
```

## Troubleshooting

- **Flask Server Issues**:
    - Ensure the Flask server is running and accessible at `http://127.0.0.1:5000`.
    - Check for errors in the Flask server console output.

- **File Permissions**:
    - Verify that the `data.json` file exists and is writable by the C# application.
    - Ensure the C# application has the necessary permissions to write to the file.

- **Dependencies**:
    - Ensure all required packages are installed, such as `Flask` for Python and `Newtonsoft.Json` for C#.

## Contributing

Feel free to fork this repository, make your changes, and submit a pull request. Contributions are welcome!

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
