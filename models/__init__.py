import boto3
import time
import json
import pika
import ssl
from datetime import datetime


def amqps(endpoint):
    host = endpoint.split('//')[1].split(':')[0]
    port = int(endpoint.split('//')[1].split(':')[1])
    return host, port


def write_json(new_data, s3_client=None, s3_bucket=None, object_key='data.json'):
    if s3_bucket is not None:
        try:
            existing_data = {}
            try:
                response = s3_client.get_object(Bucket=s3_bucket, Key=object_key)
                existing_data = json.loads(response['Body'].read().decode('utf-8'))
            except s3_client.exceptions.NoSuchKey:
                pass

            existing_data.setdefault("received_data", []).append(new_data)

            s3_client.put_object(
                Bucket=s3_bucket,
                Key=object_key,
                Body=json.dumps(existing_data, indent=4).encode('utf-8')
            )
        except Exception as e:
            print(f"Error writing JSON data to S3: {e}")
    else:
        try:
            with open('data.json', 'r') as file:
                data = json.load(file)
                data.setdefault("received_data", []).append(new_data)

            with open('data.json', 'w') as file:
                json.dump(data, file, indent=4)
        except FileNotFoundError:
            with open('data.json', 'w') as file:
                json.dump({"received_data": [new_data]}, file, indent=4)


def receive(endpoint, vhost, queue, username, password, bucket=None):
    host, port = amqps(endpoint)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=host,
            port=port,
            virtual_host=vhost,
            credentials=pika.PlainCredentials(username, password),
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
            new_data=data,
            s3_client=boto3.client('s3') if bucket else None,
            s3_bucket=bucket
        )

        print(f"\t[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] Received '{(body.decode('utf-8'))[:20]}"
              f"{'...' if len((body.decode('utf-8'))) > 20 else ''}' at '/{vhost}/{queue}'")

    try:
        channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
    except pika.exceptions.ChannelClosedByBroker:
        print(f"Queue '{queue}' doesn't exist in 'endpoint/{vhost}'. Exiting...")
        return

    print(f'Connected to {endpoint}/{vhost}/{queue}\nWaiting for messages. To exit press CTRL+C')
    channel.start_consuming()
