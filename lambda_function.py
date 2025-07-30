import os
import json
import logging
import requests
from requests.exceptions import RequestException

# Set up logging so we can see what's happening in CloudWatch
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Grab the DHL API key from environment variables
    api_key = os.getenv("DHL_API_KEY")
    if not api_key:
        # If there's no API key, we can't talk to DHL at all
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Missing DHL_API_KEY in environment"}, indent=4)
        }

    # Get the tracking number from the API request (query string)
    tracking_number = event.get("queryStringParameters", {}).get("trackingNumber")
    if not tracking_number:
    
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Missing trackingNumber"}, indent=4)
        }

    # Build the DHL API request
    url = f"https://api-eu.dhl.com/track/shipments?trackingNumber={tracking_number}"
    headers = {"DHL-API-Key": api_key, "Accept": "application/json"}

    try:
        # Call DHL API with a timeout to avoid hanging forever
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise error if response is not 200‑level
    except RequestException as e:
        # If the request itself fails (network issue, bad response, etc.)
        logger.error(f"Request failed: {e}")
        return {
            "statusCode": 502,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Failed to fetch tracking info"}, indent=4)
        }

    # Parse the JSON data DHL returned
    data = response.json()
    try:
        # Grab the list of tracking events for the shipment
        events = data["shipments"][0]["events"]

        # Find the most recent event (by timestamp)
        last_event = max(events, key=lambda e: e.get("timestamp", ""))

        # Prepare a clean result with only the key info
        result = {
            "trackingNumber": tracking_number,
            "timestamp": last_event["timestamp"],
            "description": last_event["description"]
        }
    except (KeyError, IndexError):
        result = {"trackingNumber": tracking_number, "error": "No tracking events found"}

    # Send back the result in JSON, always with status 200 if we reached this point
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(result, indent=4)
    }
