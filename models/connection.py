import pika
import json
import ssl
from .settings import *


def consume():

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=ENDPOINT,
            port=PORT,
            virtual_host=VHOST,
            credentials=pika.PlainCredentials(USERNAME, PASSWORD),
            ssl_options=pika.SSLOptions(ssl.create_default_context()),
            heartbeat=300,
            blocked_connection_timeout=300,
            connection_attempts=5,
        )
    )

    channel = connection.channel()

    def callback(ch, method, properties, body):
        data = json.loads(body.decode('utf-8'))

        # Do something with data

    try:
        channel.basic_consume(queue=QUEUE, on_message_callback=callback, auto_ack=True)

    except pika.exceptions.ChannelClosedByBroker:
        print(f"Queue '{QUEUE}' doesn't exist in 'endpoint/{VHOST}'. Exiting...")
        return

    print(f'Connected to {ENDPOINT}/{VHOST}/{QUEUE}\nWaiting for messages. To exit press CTRL+C')
    channel.start_consuming()

