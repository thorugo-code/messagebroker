import pika
import ssl


def amqps(endpoint):
    host = endpoint.split('//')[1].split(':')[0]
    port = int(endpoint.split('//')[1].split(':')[1])
    return host, port


def send(endpoint, queue, data_to_send, username, password):
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

    channel.basic_publish(exchange='', routing_key=queue, body=data_to_send)
    if len(data_to_send) < 20:
        print(f" [x] Sent '{data_to_send}' to '{queue}'")
    else:
        print(f" [x] Sent '{data_to_send[:20]}...' to '{queue}'")

    connection.close()
