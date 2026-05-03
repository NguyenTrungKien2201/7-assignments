import logging
import azure.functions as func
from shared_code.relay_direct_method import send_relay_method


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Manual relay ON request received")
    try:
        result = send_relay_method("relay_on")
        return func.HttpResponse(f"Relay ON command sent. Result: {result}", status_code=200)
    except Exception as exc:
        logging.exception("Failed to send relay_on direct method")
        return func.HttpResponse(f"Error: {exc}", status_code=500)
