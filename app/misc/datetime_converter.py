""" Coverts Datetime objects to strings to be able to log the boto3 responses with json.dump()"""
import datetime
def datetime_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
