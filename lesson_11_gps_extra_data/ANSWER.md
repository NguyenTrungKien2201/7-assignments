# Lesson 11: Investigate other GPS data

## 1. Objective

This lesson investigates GPS data beyond latitude and longitude. GPS NMEA sentences can also provide:

- UTC date and time.
- Altitude above sea level.
- Movement speed.
- Direction of travel.
- Number of satellites used for positioning.
- GPS fix quality.

## 2. Important NMEA sentences

| Sentence | Meaning | Useful data |
|---|---|---|
| GGA | Global Positioning System Fix Data | latitude, longitude, altitude, satellite count, fix quality |
| RMC | Recommended Minimum Navigation Data | UTC date, UTC time, speed, course, latitude, longitude |
| VTG | Course Over Ground and Ground Speed | course and speed |
| GSA | GNSS DOP and Active Satellites | active satellites and relative accuracy |
| GSV | Satellites in View | visible satellites |

## 3. Extra data used by the IoT device

A transport device can send extended telemetry like this:

```json
{
  "latitude": 10.7769,
  "longitude": 106.7009,
  "altitude_m": 12.4,
  "speed_kmh": 42.3,
  "gps_time_utc": "2026-05-03T09:15:20Z",
  "satellites": 8,
  "fix_quality": 1
}
```

## 4. Practical applications

- UTC date and time: synchronize device time when NTP is unavailable.
- Altitude: detect travel over hills, bridges, elevated roads, or facilities with special elevation requirements.
- Speed: detect speeding or unusual stops.
- Satellite count and fix quality: estimate how reliable the reported position is.
- Direction of travel: check whether a vehicle is following the expected route.

## 5. Source code

File:

```text
lesson_11_gps_extra_data/code/gps_extended_parser.py
```

This code manually parses several common NMEA sentence types and creates extended telemetry.

## 6. Expected result

Instead of sending only a location, the device sends speed, altitude, UTC time, and GPS signal quality. This helps a transport system track vehicles more accurately.
