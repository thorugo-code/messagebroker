from models import *

""" config.json example:

{
  "rabbitmq": {
    "username": "your-username",
    "password": "your-username-password",
    "endpoint": "amqps://your-endpoint.mq.area.amazonaws.com:port",
    "vhost": "your-vhost",
    "queue": "your-queue"
  }
}

"""

if __name__ == "__main__":

    try:
        with open('config.json', 'r') as file:
            data = json.load(file)
            user = data['rabbitmq']['username']
            password = data['rabbitmq']['password']
            endpoint = data['rabbitmq']['endpoint']
            vhost = data['rabbitmq']['vhost']
            queue = data['rabbitmq']['queue']

    except FileNotFoundError:
        raise FileNotFoundError('File config.json not found, create it with user, password and endpoint keys.')

    except KeyError:
        raise KeyError('File config.json must have user, password, endpoint, vhost and queue keys.')

    try:
        receive(endpoint, vhost, queue, user, password)
    except KeyboardInterrupt:
        print('Exiting...')
    except Exception as e:
        print(f'An error occurred: ({type(e)}) {e}. Exiting...')
