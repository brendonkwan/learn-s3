#!/usr/bin/env python3

import argparse
import boto3
import pprint

def list_keys_of_bucket_objects(bucket):
    """
    Returns a list that contains the key of each of the bucket's objects.
    If the bucket is empty, returns an empty list.
    If an error was encountered when reading the bucket, returns None.
    NOTE: Limited to returning keys of first 1000 bucket objects.
    TODO: Improve function to list all bucket objects.
    """
    s3_client = boto3.client('s3')
    try:
        response = s3_client.list_objects(Bucket=bucket)
        if len(response['Contents']) == 0:
            return None
        else:
            return [obj['Key'] for obj in response['Contents']]
    except Exception as e:
        print('The following exception occurred when listing bucket ''%s'': ' %
                bucket, end='')
        pprint.pprint(e)
        return None

def main():
    parser = argparse.ArgumentParser(description='Deletes buckets from S3')
    parser.add_argument('buckets',
            help='Name of a bucket to delete',
            metavar='B',
            nargs='+')
    parser.add_argument('--test',
            help='Test mode. If specified, no deletions will be made',
            action='store_true',
            default=False)
    args = parser.parse_args()

    s3_resource = boto3.resource('s3')

    for bucket in args.buckets:

        keys = list_keys_of_bucket_objects(bucket)

        if keys is None:
            print('Leaving bucket ''%s'' alone' % bucket)
            continue

        for key in keys:
            if args.test:
                print('Would delete object with key ''%s'' from bucket ''%s'''
                        % (key, bucket))
            else:
                print('Deleting object with key ''%s'' from bucket ''%s''' %
                        (key, bucket))
                object = s3_resource.Object(bucket_name=bucket, key=key)
                response = object.delete()
                print('Deletion response was: ', end='')
                pprint.pprint(response)

        if args.test:
            print('Would delete bucket ''%s''' % bucket)
        else:
            print('Deleting bucket ''%s''' % bucket)
            resource = boto3.resource('s3')
            resource.Bucket(bucket).delete()

if __name__ == '__main__':
    main()
