import requests
from daraja_api.conf import AbstractConfig
from daraja_api.utils import base_url

def generate_token(config:AbstractConfig):
    consumer_key = config.get_consumer_key()
    consumer_secret = config.get_consumer_secret()
    url = base_url(config)+"/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=(consumer_key, consumer_secret))
    if response.status_code != 200:
        raise Exception('Unable to generate token, status code:%s'%str(response.status_code))
    return response.json()["access_token"]
