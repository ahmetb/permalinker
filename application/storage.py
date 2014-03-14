# coding=utf-8

import os


ENV_STORAGE = 'STORAGE'

DS_AZURE = 'azure'
DS_S3 = 's3'


def get_storage():
    env = os.environ
    if ENV_STORAGE not in env:
        raise Exception('{0} key not in environment vars.'.format(ENV_STORAGE))
    ds = env[ENV_STORAGE]
    if ds == DS_AZURE:
        return get_azure_datastore()
    elif ds == DS_S3:
        return get_aws_s3_datastore()
    raise Exception('Unhandled datastore: {0}'.format(ds))


class BaseStorage():

    def upload(self, name, blob, content_type=None):
        """Uploads file to blob storage with given name and
        return a publicly accessible permalink.
        """

# Windows Azure Blob Storage


class AzureBlobStore(BaseStorage):

    client = None
    container = None

    def __init__(self, client, container):
        self.client = client
        self.container = container

        # Create container if not exists
        self.client.create_container(container, fail_on_exist=False)

        # Make container public
        self.client.set_container_acl(
            container, x_ms_blob_public_access='blob')

    def upload(self, name, blob, content_type=None):
        import azure
        self.client.put_blob(self.container, name, blob,
                             'BlockBlob', x_ms_blob_content_type=content_type)
        return 'https://{0}{1}/{2}/{3}'.format(self.client.account_name,
                                               azure.BLOB_SERVICE_HOST_BASE,
                                               self.container,
                                               name)


__azure_ds = None
__azure_ds_cachekey = None


def get_azure_datastore():
    global __azure_ds, __azure_ds_cachekey
    ENV_ACCT_NAME = 'AZURE_ACCOUNT_NAME'
    ENV_ACCT_KEY = 'AZURE_ACCOUNT_KEY'
    ENV_CONTAINER = 'AZURE_CONTAINER'
    env = os.environ

    for evar in [ENV_ACCT_NAME, ENV_ACCT_KEY, ENV_CONTAINER]:
        if evar not in env:
            raise Exception('{0} not in environment vars'.format(evar))

    ck = ENV_ACCT_NAME + ENV_ACCT_KEY + ENV_CONTAINER
    if __azure_ds and __azure_ds_cachekey == ck:
        return __azure_ds

    from azure.storage import BlobService
    ds = AzureBlobStore(BlobService(env[ENV_ACCT_NAME], env[ENV_ACCT_KEY]),
                        env[ENV_CONTAINER])
    __azure_ds = ds
    __azure_ds_cachekey = ck
    return ds


# S3 Storage

class AmazonS3Storage(BaseStorage):
    bucket_name = None
    conn = None
    bucket = None

    def __init__(self, conn, bucket_name):
        # Sanitize URL for S3 (remove '=' char of base64)
        bucket_name = bucket_name.replace('=', '')

        self.bucket_name = bucket_name
        self.conn = conn
        self.bucket = self.conn.create_bucket(bucket_name)

    def upload(self, name, blob, content_type=None):
        from boto.s3.key import Key

        k = self.bucket.new_key(name)
        if content_type:
            k.content_type = content_type
        k.set_contents_from_string(blob)
        k.set_acl('public-read')
        return k.generate_url(0, query_auth=False)

__s3_ds = None
__s3_ds_cachekey = None


def get_aws_s3_datastore():
    global __s3_ds, __s3_ds_cachekey
    ENV_ACCESS_KEY_ID = 'AWS_ACCESS_KEY_ID'
    ENV_SECRET_ACCESS_KEY = 'AWS_SECRET_ACCESS_KEY'
    ENV_S3_BUCKET = 'AWS_S3_BUCKET'

    env = os.environ

    for evar in [ENV_ACCESS_KEY_ID, ENV_SECRET_ACCESS_KEY, ENV_S3_BUCKET]:
        if evar not in env:
            raise Exception('{0} not in environment vars'.format(evar))

    ck = ENV_ACCESS_KEY_ID + ENV_SECRET_ACCESS_KEY + ENV_S3_BUCKET
    if __s3_ds and __azure_ds_cachekey == ck:
        return __s3_ds

    from boto.s3.connection import S3Connection
    conn = S3Connection(env[ENV_ACCESS_KEY_ID], env[ENV_SECRET_ACCESS_KEY])
    ds = AmazonS3Storage(conn, env[ENV_S3_BUCKET])

    __s3_ds = ds
    __s3_ds_cachekey = ck
    return ds
