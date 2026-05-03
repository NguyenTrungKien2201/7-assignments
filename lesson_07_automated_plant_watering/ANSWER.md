# Lesson 7: Automated plant watering

## 1. Objective

This lesson improves the automated watering cycle. Instead of turning the pump on for a fixed amount of time, the system estimates how many seconds of watering are needed based on the current soil moisture value.

In the soil moisture sensor used in the lesson, a higher reading means the soil is drier. The target is to bring the value back into a safe range of about `400-450`. If the reading is above `450`, the system waters the plant.

## 2. Calibration data

The table below simulates measurements taken on dry soil. After each additional second of pumping, the system waits for the water to settle and then takes another reading.

| Total pump time | Soil moisture value | Drop from previous reading |
|---:|---:|---:|
| Dry | 643 | 0 |
| 1 second | 621 | 22 |
| 2 seconds | 601 | 20 |
| 3 seconds | 579 | 22 |
| 4 seconds | 560 | 19 |
| 5 seconds | 539 | 21 |
| 6 seconds | 521 | 18 |

Total drop after 6 seconds:

```text
643 - 521 = 122 units
```

Average drop per pump second:

```text
122 / 6 = 20.33 units/second
```

Calibration conclusion:

```text
pump_rate = 20.33 soil moisture units/second
```

## 3. Watering time formula

If the sensor reports `soil_moisture = 530` and the highest acceptable target value is `450`, the system must reduce the reading by:

```text
530 - 450 = 80 units
```

The required watering time is:

```text
80 / 20.33 = 3.93 seconds
```

The value is rounded up to `4 seconds` so the plant receives enough water. To prevent overwatering, each cycle is limited to a maximum of `10 seconds`. After watering, the system waits `20 seconds` for water to soak into the soil before reading the sensor again.

## 4. Improved algorithm

1. Receive telemetry from the IoT device.
2. Read the `soil_moisture` value.
3. If `soil_moisture <= 450`, do not water.
4. If `soil_moisture > 450`:
   - Calculate `needed_drop = soil_moisture - 450`.
   - Calculate `water_seconds = ceil(needed_drop / 20.33)`.
   - Limit `water_seconds` to the range `1-10` seconds.
   - Send a command to turn the relay on.
   - Wait for `water_seconds` seconds.
   - Send a command to turn the relay off.
   - Wait `20` seconds for the soil to stabilize.
5. Continue receiving new telemetry.

## 5. Expected results

| Sensor value | Status | Expected watering time |
|---:|---|---:|
| 430 | Moist enough | 0 seconds |
| 457 | Slightly dry | 1 second |
| 500 | Dry | 3 seconds |
| 530 | Drier | 4 seconds |
| 650 | Very dry | 10 seconds, limited for safety |

## 6. Source code

The source code is located in:

```text
lesson_07_automated_plant_watering/code/improved_watering_server.py
```

This code uses MQTT to receive telemetry and send relay commands. The broker and topics can be changed in the configuration section at the top of the file.
