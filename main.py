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

    start = time.time()

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
        """
        If you want to save the data to an S3 bucket, set the bucket name here
        Else, leave it as None by default and the data will be saved to a local file
        Example: s3_bucket = 'your-bucket-name'
        """

        s3_bucket = None
        receive(endpoint, vhost, queue, user, password, bucket=s3_bucket)
    except KeyboardInterrupt:
        print('Exiting...')
    except Exception as e:
        print(f'An error occurred: ({type(e)}) {e}. Exiting...')

    print(f"Execution time: {round(time.time() - start, 2)} seconds")
