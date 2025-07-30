# dh-integration-exercise
Task 1 of DHL coding exercise
DHL Shipment Tracking Lambda

This project is a AWS Lambda function that lets you check the latest status of a DHL shipment.
It uses DHL’s Unified Tracking API and is exposed through API Gateway, so you can call it with a tracking number in the URL.

You can find latest tracking details by replacing the tracking number in this URL:
https://s4neub3op7.execute-api.us-east-1.amazonaws.com/default/getTrackingDetails?trackingNumber=4112889060
and entering it in your browser URL field.

How it works:
 You hit the API endpoint with a trackingNumber query parameter.
 The Lambda calls DHL’s Tracking API.
 It returns the most recent tracking update in JSON.

Example

Request:
GET https://s4neub3op7.execute-api.us-east-1.amazonaws.com/default/getTrackingDetails?trackingNumber=4112889060

Response:
{
    "trackingNumber": "4112889060",
    "timestamp": "2025-04-24T11:02:00+02:00",
    "description": "Delivered"
}

Error examples:
{ "error": "Missing trackingNumber" }
{ "trackingNumber": "4112889060", "error": "No tracking events found" }

Setup
1. Create a Lambda in AWS (Python 3.12 or later).
2. Add an environment variable:
   DHL_API_KEY = <your DHL API key>
3. Deploy the code from lambda_function.py.
4. Test it:
    "https://<api-id>.execute-api.us-east-1.amazonaws.com/default/getTrackingDetails?trackingNumber=4112889060"
