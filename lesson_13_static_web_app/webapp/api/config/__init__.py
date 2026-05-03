import json
import os
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    key = os.environ.get("AZURE_MAPS_KEY", "")
    return func.HttpResponse(
        json.dumps({"azureMapsKey": key}),
        mimetype="application/json",
        status_code=200,
    )
