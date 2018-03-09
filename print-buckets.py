#!/usr/bin/env python3

import boto3
from pprint import pprint

s3 = boto3.client('s3')

print("Getting list of buckets from S3")
response = s3.list_buckets()

print("Printing the response")
pprint(response)
