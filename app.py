import time
import sys
from fhict_cb_01.custom_telemetrix import CustomTelemetrix
from flask import Flask, render_template
from datetime import datetime

# Global Dependency setup
app = Flask(__name__)
board = CustomTelemetrix()

# Arduino pins declarations
BUTTON1 = 8
LDR_PIN = 2
DHT_PIN = 12

# Global variables declaration
currentLightLevel = 0
temperature = 0
humidity = 0
timestamp = 0
sensor_data = []

# Arduino callbacks
def on_ldr_changed(data):
    global currentLightLevel

    currentLightLevel = round(data[2], 2)


def on_temp_changed(data):
    global temperature, humidity, timestamp

    humidity = data[4]
    temperature = data[5]
    timestamp = data[6]


# Arduino setup
board.displayOn()
board.set_pin_mode_dht(DHT_PIN, dht_type=11,
                       callback=on_temp_changed)
board.set_pin_mode_analog_input(
    LDR_PIN, callback=on_ldr_changed, differential=50)


# Shared functions
def get_current_date_time():
    # return datetime.fromtimestamp(timestamp).strftime('%H:%M:%S.%f %d/%m/%Y')
    return datetime.now().strftime('%H:%M:%S %d/%m/%Y')


# Flask app
@app.route('/')
def home():  # put application's code here
    global sensor_data
    sensor_data.insert(0, {
        "sensor_id": "boyan_sensor_1",
        "temperature": temperature,
        "humidity": humidity,
        "brightness": currentLightLevel,
        "time_stamp": get_current_date_time(),
    })

    if len(sensor_data) >= 10:
        sensor_data.pop()

    return render_template('home.html', sensor_data=sensor_data)


if __name__ == '__main__':
    app.run()
