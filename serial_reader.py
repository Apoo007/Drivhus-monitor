import serial
import requests
import time

SERIAL_PORT = '/dev/ttyACM0'
BAUDRATE = 9600
FLASK_URL = 'http://100.105.113.76:5000/data'

ser = serial.Serial(SERIAL_PORT, BAUDRATE)
time.sleep(2)  # Vent til forbindelsen er stabil

while True:
    try:
        line = ser.readline().decode('utf-8').strip()
        print("Modtaget fra Arduino:", line)

        parts = line.split('|')

        temp = float(parts[1].split(':')[1].strip().split()[0])
        humidity = float(parts[2].split(':')[1].strip().split()[0])
        light = int(parts[3].split(':')[1].strip())
        soil = int(parts[4].split(':')[1].strip())

        sensorDry = 500
        sensorWet = 273
        maxVWC = 35.0
        soil = max(min(soil, sensorDry), sensorWet)
        vwc = (sensorDry - soil) / (sensorDry - sensorWet) * maxVWC

        data = {
            'temp': temp,
            'humidity': humidity,
            'light': light,
            'vwc': soil
        }

        requests.post(FLASK_URL, json=data)

    except Exception as e:
        print("Fejl:", e)

    time.sleep(10)
