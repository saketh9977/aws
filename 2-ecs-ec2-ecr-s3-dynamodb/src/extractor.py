import requests
import json
import boto3

from src.utils import (
    print_
)
from src.constants import *

def extract():

    print_(f"extractor-s3: fetching pincodes...")
    out = []
    s3 = boto3.resource('s3')

    content_object = s3.Object(S3_BUCKET, S3_OBJECT)
    file_content = content_object.get()['Body'].read().decode('utf-8')
    pin_code_list = json.loads(file_content)
    print_(f"extractor-s3: fetched.")

    for pin_code in pin_code_list:
        res = query_api(pin_code)
        out.append(res)

    return out

def query_api(pin_code):

    print_(f"extractor-api: {pin_code}...")
    url = f'https://api.postalpincode.in/pincode/{pin_code}'
    res = requests.get(url)
    print_(f"extractor-api: data for {pin_code} fetched")

    return json.loads(res.text)