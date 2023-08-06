import binascii
import os
import re
import threading

import boto3
import boto3.s3.transfer
import botocore.config
from botocore.exceptions import ClientError

CHUNKSIZE = 8 << 20  # 8 MB
BOTO_CONFIG = botocore.config.Config(signature_version='s3v4', retries={'max_attempts': 3})
S3_TRANSFER_CONFIG = boto3.s3.transfer.TransferConfig(io_chunksize=CHUNKSIZE)
THREAD_LOCAL = threading.local()


class S3Destination:
    """Generator yielding `store()/delete()`-able S3Files in a bucket/prefix"""
    def __init__(self, bucket, prefix=''):
        self.bucket = bucket
        self.prefix = (prefix.strip('/') + '/').lstrip('/')
        self.check_perms()
        self.delete_lock = threading.Lock()
        self.delete_keys = []

    def __iter__(self):
        s3 = create_s3_client()
        paginator = s3.get_paginator('list_objects')
        for page in paginator.paginate(Bucket=self.bucket, Prefix=self.prefix):
            for content in page.get('Contents', []):
                yield self.file(re.sub(fr'^{self.prefix}', '', content['Key']).lstrip('/'))

    def file(self, relpath):
        return S3File(self, relpath)

    def add_delete_key(self, key):
        with self.delete_lock:
            self.delete_keys.append(key)
            if len(self.delete_keys) == 1000:
                self.cleanup()

    def cleanup(self):
        if self.delete_keys:
            s3 = create_s3_client()
            delete = {'Objects': [{'Key': key} for key in self.delete_keys]}
            s3.delete_objects(Bucket=self.bucket, Delete=delete)
            self.delete_keys = []

    def check_perms(self):
        s3 = create_s3_client()
        s3.head_bucket(Bucket=self.bucket)  # s3:ListBucket
        key = self.prefix + binascii.hexlify(os.urandom(5)).decode('utf-8')
        s3.put_object(Bucket=self.bucket, Key=key, Body=b'test')  # s3:PutObject
        s3.delete_object(Bucket=self.bucket, Key=key)


class S3File:
    """Store read()-ables / delete files on S3"""
    __slots__ = ('name', 'size', 'modified', 's3dst', 'key')

    def __init__(self, s3dst, relpath):
        self.name = relpath
        self.size = None
        self.modified = None
        self.s3dst = s3dst
        self.key = f'{s3dst.prefix}{relpath}'

    def stat(self):
        s3 = create_s3_client()
        # TODO handle not exists - return False
        stat = s3.head_object(Bucket=self.s3dst.bucket, Key=self.key)
        self.size, self.modified = stat['Size'], stat['LastModified'].timestamp()
        return True

    def store(self, src_file):
        """Store `read()`-able on S3"""
        s3 = create_s3_client()
        s3.upload_fileobj(src_file, self.s3dst.bucket, self.key, Config=S3_TRANSFER_CONFIG)

    def delete(self):
        """Delete the S3 object"""
        self.s3dst.add_delete_key(self.key)


def create_s3_client():
    """Create S3 client using default credentials (per thread)"""
    if not hasattr(THREAD_LOCAL, 's3'):
        THREAD_LOCAL.s3 = boto3.client('s3', config=BOTO_CONFIG)
    return THREAD_LOCAL.s3
