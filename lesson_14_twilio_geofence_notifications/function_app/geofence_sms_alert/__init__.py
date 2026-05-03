import json
import logging
import math

import azure.functions as func


GEOFENCE_CENTER_LAT = 10.7769
GEOFENCE_CENTER_LON = 106.7009
GEOFENCE_RADIUS_METERS = 500
EARTH_RADIUS_METERS = 6_371_000


def haversine_distance_m(lat1, lon1, lat2, lon2):
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return EARTH_RADIUS_METERS * c


def main(event: func.EventHubEvent, smsMessage: func.Out[str]):
    body = json.loads(event.get_body().decode("utf-8"))
    device_id = body.get("device_id") or event.iothub_metadata.get("connection-device-id", "unknown-device")
    latitude = float(body["latitude"])
    longitude = float(body["longitude"])
    timestamp = body.get("timestamp", "unknown time")

    distance = haversine_distance_m(
        latitude,
        longitude,
        GEOFENCE_CENTER_LAT,
        GEOFENCE_CENTER_LON,
    )

    logging.info("Device %s distance from geofence center: %.2f m", device_id, distance)

    if distance <= GEOFENCE_RADIUS_METERS:
        sms = (
            f"Vehicle {device_id} entered geofence. "
            f"Distance: {distance:.1f} m. Time: {timestamp}"
        )
        smsMessage.set(sms)
        logging.info("SMS alert queued: %s", sms)
    else:
        logging.info("Vehicle outside geofence. No SMS sent.")
