import requests
from django.conf import settings

PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
BASE_URL = 'https://api.paystack.co'

def charge_authorization(email, amount_kobo, authorization_code):
    url = f"{BASE_URL}/transaction/charge_authorization"
    headers = {
        'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}',
        'Content-Type': 'application/json',
    }
    payload = {
        'email': email,
        'amount': amount_kobo,
        'authorization_code': authorization_code,
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


def transfer_to_bank(recipient_code, amount_kobo):
    url = f"{BASE_URL}/transfer"
    headers = {
        'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}',
        'Content-Type': 'application/json',
    }
    payload = {
        'source': 'balance',
        'amount': amount_kobo,
        'recipient': recipient_code,
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()
