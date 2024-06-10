import os
import ssl
import pika
import json
import boto3
from .settings import *


S3_CLIENT = boto3.client('s3') if S3_BUCKET else None
SERVICES = {
    0: 'health',
    1: 'temp',
    3: 'rms2',
    4: 'rmms',
    5: 'tilt',
    6: 'fft',
    7: 'accraw',
    9: '4t20',
    10: 'ntc',
    11: 'pot',
    'unknown': 'unknown'
}


def write_json(new_data, file, s3_client=S3_CLIENT, s3_bucket=S3_BUCKET):
    if s3_bucket and s3_client:
        existing_data = {}

        try:
            response = s3_client.get_object(Bucket=s3_bucket, Key=file)
            existing_data = json.loads(response['Body'].read().decode('utf-8'))
            if "received_data" not in existing_data:
                existing_data["received_data"] = []
            else:
                existing_data["received_data"] = existing_data["received_data"][-49:]
        except s3_client.exceptions.NoSuchKey:
            pass

        existing_data.setdefault("received_data", []).append(new_data)

        s3_client.put_object(
            Bucket=s3_bucket,
            Key=file,
            Body=json.dumps(existing_data, indent=4).encode('utf-8')
        )

    else:

        try:
            with open(f'data/{file}', 'r') as json_file:
                data = json.load(json_file)
                data.setdefault("received_data", []).append(new_data)

            with open(f'data/{file}', 'w') as json_file:
                json.dump(data, json_file, indent=4)
        except FileNotFoundError:
            if file.split('/')[0] not in os.listdir('data'):
                os.mkdir(f'data/{file.split("/")[0]}')

            with open(f'data/{file}', 'w') as json_file:
                json.dump({"received_data": [new_data]}, json_file, indent=4)


def consume():

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=HOST,
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
        write_json(
            data,
            f'{SERVICES[data.get("serviceType", "unknown")]}/{data.get("mac", "unknown")}.json'
        )

    try:
        channel.basic_consume(queue=QUEUE, on_message_callback=callback, auto_ack=True)

    except pika.exceptions.ChannelClosedByBroker:
        print(f"Queue '{QUEUE}' doesn't exist in 'endpoint/{VHOST}'. Exiting...")
        return

    print(f'Connected to {HOST}/{VHOST}/{QUEUE}\nWaiting for messages. To exit press CTRL+C')
    channel.start_consuming()
