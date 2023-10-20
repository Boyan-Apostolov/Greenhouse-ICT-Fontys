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

    filtered_data = []
    if sensor_id:
        filtered_data = [data for data in sensor_data if data["sensor_id"] == sensor_id]
    else:
        filtered_data = sensor_data

    # We show only the last 16 elements
    return list(reversed(filtered_data))[:16]


def get_view_model(sensor_id):
    global sensor_data
    sorted_data = getSensorData(sensor_id)

    view_model = {}

    if sorted_data:
        view_model = {
            "original_data": sensor_data,
            "sorted_data": sorted_data,
            "sensor_ids": list(set([data["sensor_id"] for data in sensor_data])),
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

    return view_model


@app.route('/')
def home():  # put application's code here
    view_model = get_view_model(None)

    return render_template('home.html', view_model=view_model)


@app.route("/specific-sensor/<sensor_id>")
def specific_sensor(sensor_id):
    view_model = get_view_model(sensor_id)

    return render_template('home.html', view_model=view_model, specific_sensor_id=sensor_id)


if __name__ == '__main__':
    app.run()
