#!/usr/bin/env python3

from pprint import pprint
import boto3
import tempfile

BUCKET = 'www.brendonkwan.com'
KEY = 'hello.txt'
FILEPATH = 'file_to_upload.txt'

s3 = boto3.client('s3')

print("Creating local file '%s'." % FILEPATH)
f = open(FILEPATH, 'w')
f.write('Hello\n')
f.write('world\n')
f.close()

print("Uploading local file '%s' to bucket '%s' and key '%s'." %
    (FILEPATH, BUCKET, KEY))

# NB: It's necessary to read the file in binary mode through the 'rb'
# argument. Otherwise you'll get the error message: "TypeError:
# Unicode-objects must be encoded before hashing". The error will be
# printed because the code will try to read the file's contents one
# byte at a time even though the file object will return content one
# Unicode character at a time.

f = open(FILEPATH, 'rb')
s3.upload_fileobj(f, BUCKET, KEY)
f.close()
