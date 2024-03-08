import time
from models import *
from datetime import datetime

""" config.json example:

{
  "rabbitmq": {
    "username": "your-username",
    "password": "your-username-password",
    "endpoint": "amqps://your-endpoint.mq.area.amazonaws.com:port",
    "vhost": "your-vhost",
    "queue": "your-queue"
  },
  !optional
  "aws": {
    "s3_bucket": "your-bucket-name"   
  }
}

OBS: The s3_bucket key, such as aws, is optional. If you want to save the data to an S3 bucket, set it on config.json. 
     Else, it will be saved to a local file.

"""

if __name__ == "__main__":

    start = time.time()
    errors = 0

    try:
        while True:     # Infinite loop to keep the program running
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
                s3_bucket = data.get('aws', {}).get('s3_bucket', None)
                receive(endpoint, vhost, queue, user, password, bucket=s3_bucket)
            except Exception as e:
                print(f'\t[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] An error occurred: ({type(e)}) {e}. Restarting...')
                errors += 1

    except KeyboardInterrupt:
        print(f'Execution time: {readable_time(time.time() - start)}\n{errors} errors occurred during the execution.\nExiting...')
