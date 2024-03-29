from flask import Flask, request, jsonify
import os
import json
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

app = Flask(__name__)

INFLUX_TOKEN = os.environ.get("INFLUX_TOKEN")
ORG_NAME = os.environ.get("ORG")
DB_BUCKET = os.environ.get("BUCKET")

client = InfluxDBClient(url="https://influx.mittauslaskenta.com", token=INFLUX_TOKEN)
org = ORG_NAME
bucket = DB_BUCKET
write_api = client.write_api(write_options=SYNCHRONOUS)

@app.route('/log', methods=['POST'])
def log_measurement():
    request_data = request.json
    measurements = []
    if not request_data or 'deviceId' not in request_data:
        return jsonify({'message': 'Invalid request data'}), 400
    for tag in request_data.get('tags', []):
        try:
            pressure_hpa = float(tag['pressure']) / 100.0
            data = {
                "measurement": "ruuvitag",
                "tags": {
                    "tagID": tag['id'],
                    "name": tag['name'],
                    "deviceID": request_data['deviceId']
                },
                "fields": {
                    "humidity": tag['humidity'],
                    "pressure": pressure_hpa,
                    "temperature": tag['temperature'],
                    "accelX": tag['accelX'],
                    "accelY": tag['accelY'],
                    "accelZ": tag['accelZ'],
                    "voltage": tag['voltage']
                }
            }
            measurements.append(data)
        except KeyError as e:
            return jsonify({'error': f'Missing key in request data: {str(e)}'}), 400
    try:
        write_api.write(bucket=bucket, org=org, record=measurements)
        return jsonify({'message': 'Data sent to InfluxDB Cloud successfully'}), 201
    except Exception as e:
        return jsonify({'error': f'Failed to send data to InfluxDB Cloud. Error: {str(e)}'}), 500

if __name__ == "__main__":
    app.run(debug=True)