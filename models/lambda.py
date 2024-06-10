import json
import boto3
import logging
from .settings import S3_BUCKET


logger = logging.getLogger()
logger.setLevel(logging.INFO)

S3_CLIENT = boto3.client('s3')


def read_db(file, s3_client=S3_CLIENT, s3_bucket=S3_BUCKET) -> dict | str:
    try:
        response = s3_client.get_object(Bucket=s3_bucket, Key=f'{file}.json')
        existing_data = json.loads(response['Body'].read().decode('utf-8'))
        if "received_data" not in existing_data:
            return 'Data not found!'
        else:
            try:
                return existing_data["received_data"][-1]
            except IndexError:
                return 'Waiting messages!'
    except s3_client.exceptions.NoSuchKey:
        return 'Data not found!'
    except Exception as e:
        logger.error(f"Error reading from S3: {e}")
        return str(e)


def lambda_handler(event, context):
    logger.info(f"Received event: {event}")

    try:
        path_elements = event['rawPath'].split('/')[1:]
        sensor = path_elements[1]
        service = path_elements[2]

        data = read_db(file=f'{service}/{sensor}')

        response = {
            'statusCode': 200,
            'body': json.dumps({
                'message': data
            })
        }

    except IndexError as e:
        logger.error(f"Path parameter error: {e}")
        response = {
            'statusCode': 400,
            'body': json.dumps({
                'error': 'Invalid path parameters'
            })
        }
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        response = {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }

    return response
