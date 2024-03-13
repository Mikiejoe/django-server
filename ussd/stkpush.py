
import requests
from datetime import datetime
import json
from django.conf import settings
import base64
from .models import Transaction
from .acccess_token import generate_access_token

passkey = settings.PASSKEY
# datetime.
timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
shortCode = "174379"
def createTransaction(phone, amount,reg_no):
    transaction = Transaction.objects.create(phone=phone, amount=amount, student_reg=reg_no)
    print(transaction)
    transaction.save()

def stk_push(phone, amount,reg_no):

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
        "PartyA": 25474510778,
        "PartyB": 174379,
        "PhoneNumber": phone,
        "CallBackURL": "https://django-server-hazel.vercel.app/callback/",
        "AccountReference": "FEEWIZ",
        "TransactionDesc": "Payment of X"
    }

    response = requests.request(
        "POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers=headers, json=payload)
    # print(type(response.text))
    # print(json.loads(response.text)['ResponseCode'])
    print()
    if json.loads(response.text)['ResponseCode'] == "0":
        createTransaction(phone, amount, reg_no)
        # pass
    return response.text        
# print(stkpush(254740510778, 1))
