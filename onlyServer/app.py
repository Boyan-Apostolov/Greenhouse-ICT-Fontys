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
    if len(sensor_data) >= 16:
        sensor_data.pop(0)

    return ""


# Flask app
@app.route('/')
def home():  # put application's code here
    global sensor_data

    sortedData = list(reversed(sensor_data))
    return render_template('home.html',
                           sensor_data=sensor_data,
                           sortedData=sortedData)


if __name__ == '__main__':
    app.run()
