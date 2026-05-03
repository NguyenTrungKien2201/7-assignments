import json
import logging
import os

import azure.functions as func
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod


FAN_ON_THRESHOLD = 30.0
FAN_OFF_THRESHOLD = 28.0


def send_method(device_id: str, method_name: str):
    registry_manager = IoTHubRegistryManager(os.environ["REGISTRY_MANAGER_CONNECTION_STRING"])
    method = CloudToDeviceMethod(method_name=method_name, payload="{}")
    registry_manager.invoke_device_method(device_id, method)


def main(event: func.EventHubEvent):
    body = json.loads(event.get_body().decode("utf-8"))
    device_id = event.iothub_metadata["connection-device-id"]
    temperature = float(body["temperature"])

    logging.info("Telemetry from %s: %s", device_id, body)

    if temperature >= FAN_ON_THRESHOLD:
        send_method(device_id, "fan_on")
        logging.info("fan_on sent to %s", device_id)
    elif temperature < FAN_OFF_THRESHOLD:
        send_method(device_id, "fan_off")
        logging.info("fan_off sent to %s", device_id)
    else:
        logging.info("Temperature inside hysteresis band. No command sent.")
