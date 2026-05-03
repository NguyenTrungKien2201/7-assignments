import os
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod


def send_relay_method(method_name: str):
    """Send relay_on or relay_off direct method to the configured IoT device."""
    connection_string = os.environ["REGISTRY_MANAGER_CONNECTION_STRING"]
    device_id = os.environ["DEVICE_ID"]

    registry_manager = IoTHubRegistryManager(connection_string)
    direct_method = CloudToDeviceMethod(method_name=method_name, payload="{}")
    return registry_manager.invoke_device_method(device_id, direct_method)
