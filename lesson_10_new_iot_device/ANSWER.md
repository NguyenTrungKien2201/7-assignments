# Lesson 10: Build a new IoT device

## 1. Objective

This lesson requires the design of a new IoT device with:

1. At least one sensor.
2. At least one actuator.
3. Telemetry sent to IoT Hub.
4. Cloud-to-device commands used to control the actuator.
5. An Azure Function that processes telemetry and sends direct methods.

## 2. Proposed device: Smart greenhouse fan controller

The device monitors the temperature inside a small greenhouse.

- Sensor: temperature sensor, or a virtual temperature sensor when real hardware is not available.
- Actuator: ventilation fan, simulated by a relay or LED.
- Telemetry sent to IoT Hub:

```json
{
  "temperature": 32.5,
  "humidity": 65.0,
  "device_type": "smart_greenhouse_fan"
}
```

Cloud rule:

- If `temperature >= 30`, send the direct method `fan_on`.
- If `temperature < 28`, send the direct method `fan_off`.
- The range from `28` to `30` acts as hysteresis to avoid rapid switching.

## 3. Architecture

```text
Virtual sensor/device
        |
        v
Azure IoT Hub
        |
        v
Azure Function Event Hub trigger
        |
        v
Direct method fan_on/fan_off
        |
        v
Device actuator: relay/fan/LED
```

## 4. Reason for using hysteresis

If the system used only one threshold, such as 30 degrees, the fan could turn on and off repeatedly when the temperature fluctuates around that value. This could damage the relay and make the system unstable.

Therefore, two thresholds are used:

- Turn the fan on when the temperature is at least 30 degrees.
- Turn the fan off when the temperature falls below 28 degrees.

Between 28 and 30 degrees, the current actuator state is preserved.

## 5. Security design

- The device uses its own device connection string or certificate to connect to IoT Hub.
- The function uses `REGISTRY_MANAGER_CONNECTION_STRING` with service permissions instead of an owner-level connection string when possible.
- Secrets are not hard-coded in code.
- `local.settings.json` files that contain secrets must not be committed to GitHub.

## 6. Source files

```text
lesson_10_new_iot_device/code/device/smart_greenhouse_device.py
lesson_10_new_iot_device/code/functions/greenhouse_trigger/__init__.py
lesson_10_new_iot_device/code/functions/greenhouse_trigger/function.json
```

## 7. Expected test results

| Temperature | Cloud command | Actuator state |
|---:|---|---|
| 26.5 | `fan_off` | Fan off |
| 29.0 | No change | Keep current state |
| 31.2 | `fan_on` | Fan on |
| 27.5 | `fan_off` | Fan off |
