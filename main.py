from models import send
import json


if __name__ == "__main__":
    queue = 'test'
    message = 'Testando receiver'

    try:
        with open('config.json', 'r') as file:
            data = json.load(file)
            user = data['rabbitmq']['username']
            password = data['rabbitmq']['password']
            endpoint = data['rabbitmq']['endpoint']

        send(endpoint, queue, message, user, password)

    except FileNotFoundError:
        raise FileNotFoundError('File config.json not found, create it with user, password and endpoint keys.')

