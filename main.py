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
    routine = sys.argv[1] if len(sys.argv) > 1 else 'send'

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

    if routine == 'send':
        message = json.dumps({"message": "TEST MESSAGE", "time": datetime.now().strftime("%d/%m/%Y %H:%M:%S")})
        try:
            send(endpoint, vhost, queue, message, user, password)
        except pika.exceptions.ProbableAuthenticationError:
            print('Connection error, check if the RabbitMQ is running or user has permission to access the queue.')

    elif routine == 'receive':
        try:
            receive(endpoint, vhost, queue, user, password)
        except pika.exceptions.ProbableAuthenticationError:
            print('Connection error, check if the RabbitMQ is running or user has permission to access the queue.')
        except KeyboardInterrupt:
            print('Exiting...')
