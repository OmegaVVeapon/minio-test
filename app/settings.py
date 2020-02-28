import os

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

SOURCE_MEDIA_LOCATION = os.getenv('SOURCE_MEDIA_LOCATION', '/tmp/source.mp4')

# S3 stuff

ACCESS_KEY_ID = os.getenv('ACCESS_KEY_ID')
SECRET_ACCESS_KEY = os.getenv('SECRET_ACCESS_KEY')
BUCKET = os.getenv('BUCKET')
REGION = os.getenv('REGION')
ENDPOINT_URL = os.getenv('ENDPOINT_URL')
