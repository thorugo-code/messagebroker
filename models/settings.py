from decouple import config


"""
Important: Need to create a file named .env with configuration variables.
The module decouple is used to read the .env file. 
Config function is used to read the variables by name.
"""


USERNAME = config('RABBITMQ_USER', default='admin')
PASSWORD = config('RABBITMQ_PASSWORD', default='admin')
HOST = config('RABBITMQ_HOST', default='localhost')
PORT = config('RABBITMQ_PORT', default='5672')
VHOST = config('RABBITMQ_VHOST', default='/')
QUEUE = config('RABBITMQ_QUEUE', default='default')
S3_BUCKET = config('S3_BUCKET', default=None)
API_PORT = int(config('API_PORT', default=8000))
API_URL = config('API_URL', default='localhost')
