# coding=utf-8

import os


ENV_STORAGE = 'STORAGE'

DS_AZURE = 'azure'


def get_storage():
    env = os.environ
    if ENV_STORAGE not in env:
        raise Exception('{0} key not in environment vars.'.format(ENV_STORAGE))
    ds = env[ENV_STORAGE]
    if ds == DS_AZURE:
        return get_azure_datastore()
    raise Exception('Unhandled datastore: {0}'.format(ds))


class BaseStorage():

    def upload(name, blob):
        """Uploads file to blob storage with given name and
        return a publicly accessible permalink.
        """


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

    def upload(self, name, blob, content_type):
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

    if ENV_ACCT_NAME not in env:
        raise Exception('{0} not in environment vars'.format(ENV_ACCT_NAME))
    if ENV_ACCT_KEY not in env:
        raise Exception('{0} not in environment vars'.format(ENV_ACCT_KEY))
    if ENV_CONTAINER not in env:
        raise Exception('{0} not in environment vars'.format(ENV_CONTAINER))

    ck = ENV_ACCT_NAME + ENV_ACCT_KEY + ENV_CONTAINER
    if __azure_ds and __azure_ds_cachekey == ck:
        return __azure_ds

    from azure.storage import BlobService
    ds = AzureBlobStore(BlobService(env[ENV_ACCT_NAME], env[ENV_ACCT_KEY]),
                        env[ENV_CONTAINER])
    __azure_ds = ds
    __azure_ds_cachekey = ck
    return ds

