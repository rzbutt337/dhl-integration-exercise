import os
import json
import requests

def lambda_handler(event, context):
    api_key = os.getenv("DHL_API_KEY")
    tracking_number = event.get("queryStringParameters", {}).get("trackingNumber")

    if not tracking_number:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Missing trackingNumber"}, indent=4)
        }

    url = f"https://api-eu.dhl.com/track/shipments?trackingNumber={tracking_number}"
    headers = {"DHL-API-Key": api_key, "Accept": "application/json"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {
            "statusCode": response.status_code,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": response.text}, indent=4)
        }

    data = response.json()
    try:
        events = data["shipments"][0]["events"]
        last_event = events[0]
        result = {
            "trackingNumber": tracking_number,
            "timestamp": last_event["timestamp"],
            "description": last_event["description"]
        }
    except (KeyError, IndexError):
        result = {"trackingNumber": tracking_number, "error": "No tracking events found"}

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(result, indent=4) 
    }
