import requests
from datetime import datetime
from django.conf import settings
import base64


def generate_access_token():
    consumer_key = settings.CONSUMER_KEY
    consumer_secret = settings.CONSUMER_SECRET
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    try:
        encoded_credentials = base64.b64encode(
            f"{consumer_key}:{consumer_secret}".encode()).decode()
        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json"
        }
        # Send the request and parse the response
        response = requests.get(url, headers=headers).json()
        # name = json
        # Check for errors and return the access token
        if "access_token" in response.keys():
            return response["access_token"]
        else:
            raise Exception("Failed to get access token: " +
                            response["error_description"])
    except Exception as e:
        raise Exception("Failed to get access token: " + str(e))

# +254 795 290373
