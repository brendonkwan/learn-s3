#!/usr/bin/env python3

from pprint import pprint
import boto3

BUCKET = 'www.brendonkwan.com'
KEY = 'hello.txt'
FILEPATH = 'file_downloaded.txt'

s3 = boto3.resource('s3')

print("Downloading to local file '%s' the object identified by bucket '%s' and key '%s'." %
    (FILEPATH, BUCKET, KEY))
s3.Bucket(BUCKET).download_file(KEY, FILEPATH)
