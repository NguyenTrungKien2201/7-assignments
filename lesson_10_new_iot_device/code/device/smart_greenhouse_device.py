"""
Lesson 10 - Virtual smart greenhouse IoT device.

The device sends temperature/humidity telemetry to Azure IoT Hub and handles
cloud direct methods fan_on and fan_off.

Environment variable required:
    IOTHUB_DEVICE_CONNECTION_STRING
"""

import json
import os
import random
import time
from datetime import datetime, timezone

from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse


fan_state = False


def create_client() -> IoTHubDeviceClient:
    connection_string = os.environ["IOTHUB_DEVICE_CONNECTION_STRING"]
    client = IoTHubDeviceClient.create_from_connection_string(connection_string)
    client.on_method_request_received = handle_method_request
    return client


def handle_method_request(method_request):
    global fan_state

    if method_request.name == "fan_on":
        fan_state = True
        payload = {"result": "fan turned on", "fan_on": fan_state}
        status = 200
    elif method_request.name == "fan_off":
        fan_state = False
        payload = {"result": "fan turned off", "fan_on": fan_state}
        status = 200
    else:
        payload = {"error": f"Unknown method: {method_request.name}"}
        status = 404

    response = MethodResponse.create_from_method_request(method_request, status, payload)
    client.send_method_response(response)
    print("Direct method handled:", method_request.name, payload)


def read_virtual_sensor():
    temperature = round(random.uniform(24.0, 34.0), 2)
    humidity = round(random.uniform(55.0, 80.0), 2)
    return temperature, humidity


def send_telemetry(client: IoTHubDeviceClient):
    temperature, humidity = read_virtual_sensor()
    payload = {
        "device_type": "smart_greenhouse_fan",
        "temperature": temperature,
        "humidity": humidity,
        "fan_on": fan_state,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    message = Message(json.dumps(payload))
    message.content_encoding = "utf-8"
    message.content_type = "application/json"
    client.send_message(message)
    print("Telemetry sent:", payload)


client = create_client()

try:
    print("Smart greenhouse device started")
    while True:
        send_telemetry(client)
        time.sleep(10)
except KeyboardInterrupt:
    print("Stopping device")
finally:
    client.shutdown()
