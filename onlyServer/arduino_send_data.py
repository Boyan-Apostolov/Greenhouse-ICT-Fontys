import time
import sys
from fhict_cb_01.custom_telemetrix import CustomTelemetrix
from datetime import datetime
import requests


board = CustomTelemetrix()

# -----------
# Constants
# -----------
BUTTON1 = 8
LDR_PIN = 2
DHTPIN = 12  # digital pin
# -----------
# functions
# -----------

def getCurrentDateTime():
    # return datetime.fromtimestamp(timestamp).strftime('%H:%M:%S.%f %d/%m/%Y')
    return datetime.now().strftime('%H:%M:%S %d/%m/%Y')

currentLightLevel = 0
def LDRChanged(data):
    global currentLightLevel
    
    currentLightLevel = round(data[2], 2)

temperature = 0
humidity = 0
timestamp = 0
def TempChanged(data):
    global temperature, humidity,timestamp
    
    humidity = data[4]
    temperature = data[5]
    timestamp = data[6]
    
    

def setup():
    board.displayOn()
    
    board.set_pin_mode_dht(DHTPIN, dht_type=11,
                           callback=TempChanged)
    
    board.set_pin_mode_analog_input(
    LDR_PIN, callback=LDRChanged, differential=50)


data = []
def loop():
    global temperature, humidity, currentLightLevel, timestamp, data
    latestData = {
        "sensor_id": "boyan_sensor_1",
        "temperature": temperature,
        "humidity": humidity,
        "brightness": currentLightLevel,
        "time_stamp" : getCurrentDateTime(),
    }
    
    data.append(latestData)

    try:
        print(latestData)
        
        request = requests.post("http://127.0.0.1:5000/receive_data", json=latestData)
        
        if request.status_code != 200:
            print(f"Post request failed! Error code: {request.status_code}")
    except requests.exceptions.HTTPError as err:
        print(err)
    
    time.sleep(5)

# --------------
# main program
# --------------
setup()
while True:
    try:
        loop()
    except KeyboardInterrupt:  # crtl+C
        print('shutdown')
        board.shutdown()
        sys.exit(0)
