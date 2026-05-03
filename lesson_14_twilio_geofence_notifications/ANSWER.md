# Lesson 14: Send notifications using Twilio

## 1. Objective

This lesson adds an SMS or email notification when GPS coordinates are inside or outside a geofence. This submission uses Twilio SMS when the vehicle enters the geofence.

Conditions:

- Send a notification only when the vehicle is inside the geofence.
- Do not send notifications for both inside and outside conditions at the same time.
- Use an Azure Functions binding for Twilio SMS.

## 2. Architecture

```text
GPS telemetry from IoT Hub
        |
        v
Azure Function Event Hub trigger
        |
        v
Check geofence condition
        |
        v
Twilio SMS output binding
        |
        v
Recipient phone number
```

## 3. Sample geofence

The sample geofence center is in central Ho Chi Minh City:

```text
center_latitude = 10.7769
center_longitude = 106.7009
radius_meters = 500
```

If the distance from the vehicle to the center is less than or equal to `500 m`, the vehicle is considered inside the geofence.

## 4. Distance formula

The Haversine formula is used to calculate the distance between two latitude/longitude coordinate pairs on the surface of the Earth.

Steps:

1. Convert degrees to radians.
2. Calculate the latitude and longitude differences.
3. Apply the Haversine formula.
4. Multiply by the Earth's radius to get meters.

## 5. Required environment variables

| Variable | Purpose |
|---|---|
| `TwilioAccountSid` | Twilio account SID |
| `TwilioAuthToken` | Twilio authentication token |
| `TwilioFromNumber` | Twilio sender phone number |
| `AlertToNumber` | Recipient phone number for alerts |
| `IOT_HUB_CONNECTION_STRING` | Connection string used by the Azure Function to read telemetry |

## 6. Processing logic

1. The function receives GPS telemetry from IoT Hub.
2. It reads `latitude`, `longitude`, `device_id`, and `timestamp`.
3. It calculates the distance to the geofence center.
4. If `distance <= 500`, it creates an SMS message.
5. If the vehicle is outside the geofence, it only logs the result and does not send SMS.

## 7. Source files

```text
lesson_14_twilio_geofence_notifications/function_app/geofence_sms_alert/__init__.py
lesson_14_twilio_geofence_notifications/function_app/geofence_sms_alert/function.json
```

## 8. Expected result

When the vehicle enters the geofence, the recipient receives an SMS like:

```text
Vehicle vehicle-001 entered geofence. Distance: 214.7 m. Time: 2026-05-03T09:10:00Z
```

When the vehicle is outside the geofence, the function writes a log message and does not send SMS.
