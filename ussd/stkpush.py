
import requests
from datetime import datetime
from django.conf import settings
import base64

from ussd.acccess_token import generate_access_token

passkey = settings.PASSKEY
timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
shortCode = "174379"


def stkpush(phone, amount):

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {generate_access_token()}'
    }

    payload = {
        "BusinessShortCode": 174379,
        "Password": base64.b64encode((shortCode + passkey + timestamp).encode('utf-8')).decode('utf-8'),
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": 254740510778,
        "PartyB": 174379,
        "PhoneNumber": phone,
        "CallBackURL": "https://21bdbn4c-8000.uks1.devtunnels.ms/",
        "AccountReference": "FEEWIZ",
        "TransactionDesc": "Payment of X"
    }

    response = requests.request(
        "POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers=headers, json=payload)
