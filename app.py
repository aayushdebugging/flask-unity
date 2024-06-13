from flask import Flask, jsonify
import time
import random
import json
import threading

app = Flask(__name__)

# Path to store data
DATA_FILE = 'data.json'

# Lock for thread safety
data_lock = threading.Lock()

# Function to write single data entry to the file
def write_data(data):
    with data_lock:
        try:
            with open(DATA_FILE, 'w') as file:  # Open file in write mode
                json.dump(data, file)
        except IOError as e:
            print(f"Error writing to file: {e}")

# Simulated data update function
def generate_data():
    while True:
        oxygen_level = random.randint(0, 100)
        pollutant_level = random.randint(0, 100)

        # Determine color based on oxygen level
        red = min(255, int(255 * (100 - oxygen_level) / 100))
        green = min(255, int(255 * oxygen_level / 100))
        blue = 0
        color = f"rgb({red}, {green}, {blue})"

        # Determine size based on pollutant level (range from 0.1 to 1)
        size = 0.1 + (pollutant_level / 100) * 0.9  # Scale pollutant_level to range from 0.1 to 1

        data = {
            'oxygen_level': oxygen_level,
            'pollutant_level': pollutant_level,
            'size': size,
            'color': color
        }

        # Print to console
        print(data)

        # Write data to file
        write_data(data)

        # Wait for a second before next update
        time.sleep(1)

# Endpoint to provide the latest JSON data
@app.route('/api/update', methods=['GET'])
def update_data():
    with data_lock:
        try:
            with open(DATA_FILE, 'r') as file:
                # Read the content of the file
                data = json.load(file)
                return jsonify(data)
        except IOError as e:
            return jsonify({"error": f"Error reading file: {e}"}), 500

# Start the data generation in a separate thread
def start_data_generation():
    thread = threading.Thread(target=generate_data)
    thread.daemon = True  # Allow program to exit even if thread is still running
    thread.start()

if __name__ == "__main__":
    start_data_generation()
    app.run(debug=True)
