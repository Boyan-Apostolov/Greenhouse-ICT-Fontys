import time
import sys
from flask import Flask, render_template, request
from datetime import datetime

# Global Dependency setup
app = Flask(__name__)

sensor_data = []


@app.route("/receive_data", methods=["POST"])
def receive_data():
    global sensor_data

    receiveData = request.get_json()
    requiredKeys = ['sensor_id', "temperature", "humidity", "brightness", "time_stamp"]
    allKeysExist = all(key in receiveData for key in requiredKeys)

    if not allKeysExist:
        errorMsg = "Not all required keys are present!"
        print(errorMsg)
        return errorMsg, 500

    sensor_data.append(receiveData)

    countOfResults = sum(1 for data in sensor_data if data["sensor_id"] == receiveData["sensor_id"])

    # We allow up to 16 results from a sensor
    if countOfResults >= 16:
        sensor_data.pop(0)

    return ""


def getSensorData(sensor_id):
    global sensor_data

    if sensor_id:
        # filter by sensor data
        print('test')

    # We show only the last 16 elements
    return list(reversed(sensor_data))[:16]


# Flask app
@app.route('/')
def home():  # put application's code here
    global sensor_data

    sortedData = getSensorData(None)

    view_model = {
        "original_data": sensor_data,
        "sorted_data": sortedData,
        "average_temp": 0,
        "temperature":
            {
                "average": round(
                    sum(data["temperature"] for data in sensor_data) / len(sensor_data), 2
                ),
                "min": round(
                    min(data["temperature"] for data in sensor_data), 2
                ),
                "max": round(
                    max(data["temperature"] for data in sensor_data), 2
                )
            },
        "humidity":
            {
                "average": round(
                    sum(data["humidity"] for data in sensor_data) / len(sensor_data), 2
                ),
                "min": round(
                    min(data["humidity"] for data in sensor_data), 2
                ),
                "max": round(
                    max(data["humidity"] for data in sensor_data), 2
                )
            }
    }
    return render_template('home.html', view_model=view_model)


@app.route("/specific-sensor/<sensor_id>")
def specific_sensor(sensor_id):
    return "404"


if __name__ == '__main__':
    app.run()
