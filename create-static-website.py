#!/usr/bin/env python3

import boto3

BUCKET_WEBSITE = 'static.brendonkwan.com'
INDEX_FILE = 'static-website/index.txt'
INDEX_KEY = 'index.txt'
ERROR_FILE = 'static-website/error.txt'
ERROR_KEY = 'error.txt'
REGION = 'ap-southeast-2'

s3 = boto3.resource('s3')

print('Creating bucket website "%s".' % (BUCKET_WEBSITE))
bucket_website = s3.BucketWebsite(BUCKET_WEBSITE)
try:
    bucket_website.Bucket().create(
        CreateBucketConfiguration={
            'LocationConstraint': REGION
        }
    )
except Exception as e:
    print('Exception: %s' % e)
    
print('Setting index document to key "%s" and error document to key "%s".' %
    (INDEX_KEY, ERROR_KEY))
bucket_website.put(
    WebsiteConfiguration={
        'IndexDocument': {'Suffix': INDEX_KEY},
        'ErrorDocument': {'Key': ERROR_KEY}
    }
)

print('Making the bucket''s contents private')
bucket_website.Bucket().Acl().put(ACL='private')

print('Uploading index file "%s" to public key "%s".' % (INDEX_FILE, INDEX_KEY))
bucket_website.Bucket().put_object(
    ACL='public-read',
    Body=open(INDEX_FILE, 'rb'),
    Key=INDEX_KEY
)

print('Uploading error file "%s" to public key "%s".' % (ERROR_FILE, ERROR_KEY))
bucket_website.Bucket().put_object(
    ACL='public-read',
    Body=open(ERROR_FILE, 'rb'),
    Key=ERROR_KEY
)

print('Static website is available at http://%s.s3-website-%s.amazonaws.com' %
    (BUCKET_WEBSITE, REGION)
)
