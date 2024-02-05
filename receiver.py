from datetime import datetime
import pika
import json
import ssl


def amqps(endpoint):
    host = endpoint.split('//')[1].split(':')[0]
    port = int(endpoint.split('//')[1].split(':')[1])
    return host, port


def write_json(new_data, filename='data.json'):
    try:
        with open(filename, 'r+') as file:
            file_data = json.load(file)
            file_data["received_data"].append(new_data)
            file.seek(0)
            json.dump(file_data, file, indent=4)

    except FileNotFoundError:
        with open(filename, 'w') as file:
            data = dict()
            data['received_data'] = [new_data]
            json.dump(data, file, indent=4)


def receive(endpoint, queue, username, password):
    host, port = amqps(endpoint)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host, port, '/',
            pika.PlainCredentials(username, password),
            ssl_options=pika.SSLOptions(ssl.create_default_context())
        )
    )

    channel = connection.channel()
    channel.queue_declare(queue=queue)

    def callback(ch, method, properties, body):
        write_json({"message": body.decode('utf-8'), "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")})
        print(f" [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] Received '{body[:20]}...' to '{queue}'")

    channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == "__main__":
    queue = 'test'

    try:
        with open('config.json', 'r') as file:
            data = json.load(file)
            user = data['rabbitmq']['username']
            password = data['rabbitmq']['password']
            endpoint = data['rabbitmq']['endpoint']

        receive(endpoint, queue, user, password)

    except FileNotFoundError:
        raise FileNotFoundError('File config.json not found, create it with user, password and endpoint keys.')

    except KeyboardInterrupt:
        print('Exiting...')
