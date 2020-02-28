import logging
import json
import boto3
from botocore.exceptions import ClientError
from app import settings
from app.misc.progress_percentage import ProgressPercentage
from app.misc.datetime_converter import datetime_converter

NUMERIC_LOG_LEVEL = getattr(logging, settings.LOG_LEVEL.upper(), None)

if not isinstance(NUMERIC_LOG_LEVEL, int):
    raise ValueError('Invalid log level: %s' % settings.LOG_LEVEL)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=NUMERIC_LOG_LEVEL
        )
LOG = logging.getLogger(__name__)

# Set the logging level for boto3
boto3.set_stream_logger('boto3.resources', logging.INFO)

LOG.info("Initializing session")
SESSION = boto3.session.Session()

LOG.info("Initializing client")
CLIENT = SESSION.client('s3',
                        region_name=settings.REGION,
                        endpoint_url=settings.ENDPOINT_URL,
                        aws_access_key_id=settings.ACCESS_KEY_ID,
                        aws_secret_access_key=settings.SECRET_ACCESS_KEY)

def create_bucket():
    response = {}
    try:
        response = CLIENT.create_bucket(ACL='public-read',
                                        Bucket=settings.BUCKET)
    except ClientError as error:
        if error.response['Error']['Code'] == 'BucketAlreadyOwnedByYou' or error.response['Error']['Code'] == 'BucketAlreadyExists':
            LOG.info("Bucket %s already exists, skiping", settings.BUCKET)
        else:
            LOG.error("ClientError: %s when creating bucket %s", error, settings.BUCKET)
            raise error
    return json.dumps(response)

def list_objects(prefix=''):
    """Return a list of files in the configured S3 bucket"""
    contents = list()
    response = CLIENT.list_objects_v2(Bucket=settings.BUCKET,
                                  Prefix=prefix)

    return json.dumps(response, indent=4, default = datetime_converter)
    #  try:
    #      for obj in response['Contents']:
    #          contents.append({'Key': obj['Key']})
    #  except KeyError:
    #      LOG.info("There are no uploaded files in %s", prefix)

    #  return contents

def upload_file(source_path, dest_path):
    """Upload a single file to a destination path in the S3 bucket with
    some optional args"""

    response = {}

    try:
        response = CLIENT.upload_file(Filename=source_path,
                                      Bucket=settings.BUCKET,
                                      Key=dest_path,
                                      Callback=ProgressPercentage(source_path))
    except ClientError as error:
        LOG.error("ClientError: %s for media %s", error, source_path)
        raise error
    return response

def copy_object(acl, source_dict, dest_path, metadata=None):

    copy_kwargs = {}

    if metadata:
        copy_kwargs['Metadata'] = {
            'Content-Type' : 'video/mp4'
        }

    try:
        response = CLIENT.copy_object(ACL=acl,
                                      CopySource=source_dict,
                                      #  ContentType='video/mp4',
                                      Bucket=settings.BUCKET,
                                      Key=dest_path,
                                      MetadataDirective='REPLACE',
                                      Metadata={'Content-Type' : 'video/mp4'},
                                      #  **copy_kwargs
                                      )
    except ClientError as error:
        LOG.error("ClientError: %s for media %s", error, source_dict)
        raise error
    return response


# main

LOG.info("Creating %s bucket", settings.BUCKET)
create_bucket()
LOG.info("The objects in the bucket are currently:\n %s", list_objects())
LOG.info("Starting upload...")
upload_file(source_path=settings.SOURCE_MEDIA_LOCATION,
            dest_path="medias/something.mp4")
LOG.info("The objects in the bucket are currently:\n %s", list_objects())
# Replace the existing object to add the Content-Type metadata
LOG.info("Copying the object to the same location to add the metadata")
copy_object(acl='public-read',
            source_dict={
                'Bucket': settings.BUCKET,
                'Key': 'medias/something.mp4'
                },
            dest_path='medias/something.mp4'
           )
LOG.info("The objects in the bucket are currently:\n %s", list_objects())
