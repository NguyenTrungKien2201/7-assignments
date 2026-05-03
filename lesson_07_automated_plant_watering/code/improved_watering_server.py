"""
Lesson 07 - Improved automated watering server.

This server receives soil moisture telemetry over MQTT and controls a relay
with a calculated watering duration instead of a fixed 5-second duration.

Run:
    pip install -r requirements.txt
    python improved_watering_server.py
"""

import json
import math
import threading
import time
from dataclasses import dataclass

import paho.mqtt.client as mqtt


@dataclass
class WateringConfig:
    broker: str = "test.mosquitto.org"
    client_id: str = "student_soilmoisturesensor_server"
    telemetry_topic: str = "student/soil-moisture/telemetry"
    command_topic: str = "student/soil-moisture/commands"
    target_max: int = 450
    moisture_drop_per_second: float = 20.33
    max_water_seconds: int = 10
    stabilization_seconds: int = 20


config = WateringConfig()
watering_lock = threading.Lock()


def calculate_water_time(current_moisture: float) -> int:
    """Return the number of seconds the pump should run."""
    if current_moisture <= config.target_max:
        return 0

    needed_drop = current_moisture - config.target_max
    seconds = math.ceil(needed_drop / config.moisture_drop_per_second)
    return max(1, min(seconds, config.max_water_seconds))


def send_relay_command(client: mqtt.Client, relay_on: bool) -> None:
    payload = {"relay_on": relay_on}
    print("Sending command:", payload)
    client.publish(config.command_topic, json.dumps(payload))


def control_relay(client: mqtt.Client, seconds: int) -> None:
    """Turn relay on for the calculated number of seconds, then wait for stabilization."""
    if not watering_lock.acquire(blocking=False):
        print("Watering cycle already running. Ignoring overlapping telemetry.")
        return

    try:
        print(f"Watering for {seconds} second(s)")
        client.unsubscribe(config.telemetry_topic)
        send_relay_command(client, True)
        time.sleep(seconds)
        send_relay_command(client, False)
        print(f"Waiting {config.stabilization_seconds} seconds for water to soak into soil")
        time.sleep(config.stabilization_seconds)
        client.subscribe(config.telemetry_topic)
    finally:
        watering_lock.release()


def on_connect(client: mqtt.Client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(config.telemetry_topic)
    else:
        print("MQTT connection failed with code", rc)


def on_message(client: mqtt.Client, userdata, message):
    try:
        payload = json.loads(message.payload.decode("utf-8"))
        soil_moisture = float(payload["soil_moisture"])
    except (json.JSONDecodeError, KeyError, ValueError) as exc:
        print("Invalid telemetry:", message.payload, exc)
        return

    print("Telemetry received:", payload)
    seconds = calculate_water_time(soil_moisture)

    if seconds == 0:
        print("Soil moisture is acceptable. No watering needed.")
        return

    threading.Thread(target=control_relay, args=(client, seconds), daemon=True).start()


def main():
    client = mqtt.Client(config.client_id)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(config.broker)
    client.loop_forever()


if __name__ == "__main__":
    main()
