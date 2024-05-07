import requests
from .settings import API_URL, API_PORT


API_ENDPOINT = f"{API_URL}:{API_PORT}"
data = '** POST data **'


def post():
    try:
        r = requests.post(url=API_ENDPOINT, data=data)
        print(f"Response: {r.text}\n")
    except requests.exceptions.ConnectionError:
        print(f"Connection error. Could not connect to {API_ENDPOINT}")

