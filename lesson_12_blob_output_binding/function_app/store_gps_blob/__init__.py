import json
from datetime import datetime, timezone

import azure.functions as func


def main(event: func.EventHubEvent, outputBlob: func.Out[str]):
    body = json.loads(event.get_body().decode("utf-8"))
    device_id = event.iothub_metadata.get("connection-device-id", "unknown-device")

    blob_document = {
        "device_id": device_id,
        "received_at_utc": datetime.now(timezone.utc).isoformat(),
        "telemetry": body,
    }

    outputBlob.set(json.dumps(blob_document, indent=2))
