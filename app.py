from flask import Flask, request, jsonify
import mysql.connector
from datetime import time
import os

app = Flask(__name__)

def save_to_mariadb(data):
    try:
        conn = mysql.connector.connect(
            host="mariadb",
            user="root",
            password="123",
            database="plant_monitor",
            port=3306
        )
        cursor = conn.cursor()

        query = """
        INSERT INTO plant_data (
            plant_id, timestamp, temperature_celsius, humidity_percent, soil_moisture_percent, light_lux
        ) VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (
            1,                         # plant_id
            data['timestamp'],         # timestamp string i ISO-format
            data['temp'],              # temperature_celsius
            data['humidity'],          # humidity_percent
            data['vwc'],               # soil_moisture_percent ← vigtig ændring!
            data['light']              # light_lux
        ))

        conn.commit()
        cursor.close()
        conn.close()
        print("Data gemt i MariaDB")
    except Exception as e:
        print("Fejl ved database:", e)

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    print("🔹 Received:", data, flush=True)
 try:
        conn = mysql.connector.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            user=os.environ.get("DB_USER", "root"),
            password=os.environ.get("DB_PASSWORD", ""),
            database=os.environ.get("DB_NAME", "plant_monitor")
        )
        cursor = conn.cursor()

        insert_query = """
            INSERT INTO plant_data (plant_id, timestamp, temperature_celsius, humidity_percent, soil_moisture_percent, light_lux)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            data["plant_id"],
            data["timestamp"],
            data["temperature_celsius"],
            data["humidity_percent"],
            data["soil_moisture_percent"],
            data["light_lux"]
        ))

        conn.commit()
        cursor.close()
        conn.close()

        print("Inserted data successfully", flush=True)
        return jsonify({"status": "Data gemt"})

    except Exception as e:
        print("ERROR:", e, flush=True)
        return jsonify({"status": "Database error", "error": str(e)}), 500
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
