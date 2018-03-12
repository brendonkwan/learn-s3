#!/usr/bin/env python3

import argparse
import boto3
import http
import pprint

def list_keys_of_bucket_objects(bucket_name):
    """
    Returns a list that contains the key of each of the bucket's objects.
    If the bucket is empty, returns an empty list.
    NOTE: Limited to returning keys of first 1000 bucket objects.
    TODO: Improve function to check for more pages of results.
    """
    
    print('Looking for the objects of bucket "%s"' % bucket_name)
    response = boto3.client('s3').list_objects(Bucket=bucket_name)
    if 'Contents' not in response:
        return []
    else:
        return [obj['Key'] for obj in response['Contents']]


def delete_objects_of_bucket(bucket_name, test_mode):
    for key in list_keys_of_bucket_objects(bucket_name):
        if test_mode:
            print('Would delete object with key "%s" from bucket "%s"'
                    % (key, bucket_name))
        else:
            print('Deleting object with key "%s" from bucket "%s"' %
                    (key, bucket_name))
            object = boto3.resource('s3').Object(bucket_name=bucket_name,
                    key=key)
            response = object.delete()
            if response['ResponseMetadata']['HTTPStatusCode'] != http.HTTPStatus.NO_CONTENT:
                print('Error during deletion. Response was:')
                pprint.pprint(response)


def delete_bucket(bucket_name, test_mode):
    if test_mode:
        print('Would delete bucket "%s"' % bucket_name)
    else:
        print('Deleting bucket "%s"' % bucket_name)
        boto3.resource('s3').Bucket(bucket_name).delete()


def main():
    parser = argparse.ArgumentParser(description='Deletes buckets from S3')
    parser.add_argument('bucket_names',
            help='Name of a bucket to delete',
            metavar='BUCKET_NAME',
            nargs='+')
    parser.add_argument('--test',
            help='Test mode. If specified, no deletions will be made',
            action='store_true',
            default=False)
    args = parser.parse_args()

    for bucket_name in args.bucket_names:
        # All objects in the bucket must be deleted before the bucket itself
        # can be deleted.
        delete_objects_of_bucket(bucket_name, args.test)
        delete_bucket(bucket_name, args.test)


if __name__ == '__main__':
    main()
