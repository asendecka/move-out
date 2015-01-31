# custom_storages.py
from django.conf import settings
from storages.backends.s3boto import S3BotoStorage

class MediaStorage(S3BotoStorage):
    pass
