from flask import Flask, jsonify
import time
import random
import threading

app = Flask(__name__)

data = {}

def generate_data():
    while True:
        for key in list(data.keys()):
            oxygen_level = random.randint(0, 100)
            pollutant_level = random.randint(0, 100)

            red = min(255, int(255 * (100 - oxygen_level) / 100))
            green = min(255, int(255 * oxygen_level / 100))
            blue = 0
            color = f"rgb({red}, {green}, {blue})"

            size = 0.1 + (pollutant_level / 100) * 0.9

            data[key].update({
                'oxygen_level': oxygen_level,
                'pollutant_level': pollutant_level,
                'size': size,
                'color': color
            })
        
        time.sleep(1)

def add_new_variable():
    count = 1
    while True:
        longitude = random.uniform(-180, 180)
        latitude = random.uniform(-90, 90)
        key = f"variable_{count}"
        data[key] = {
            'longitude': longitude,
            'latitude': latitude,
            'oxygen_level': 0,
            'pollutant_level': 0,
            'size': 0,
            'color': "rgb(0, 0, 0)"
        }
        count += 1
        time.sleep(5)

@app.route('/api/update', methods=['GET'])
def update_data():
    return jsonify(data)

if __name__ == "__main__":
    threading.Thread(target=generate_data).start()
    threading.Thread(target=add_new_variable).start()
    app.run(debug=True)
