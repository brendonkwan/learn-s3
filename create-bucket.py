#!/usr/bin/env python3

import boto3
from pprint import pprint

s3 = boto3.client('s3')

bucket_spec = {
    'Bucket': 'www.brendonkwan.com',
    'CreateBucketConfiguration': {
        'LocationConstraint': 'ap-southeast-2'
    }
}

print("About to create a bucket using the following specification:")
pprint(bucket_spec)

s3.create_bucket(**bucket_spec)
