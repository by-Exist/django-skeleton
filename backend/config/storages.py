import environ
from storages.backends.s3boto3 import S3Boto3Storage


env = environ.Env()


class StaticStorage(S3Boto3Storage):
    bucket_name = env.str("DJANGO_STATIC_STORAGE_BUCKET_NAME")


class MediaStorage(S3Boto3Storage):
    bucket_name = env.str("DJANGO_MEDIA_STORAGE_BUCKET_NAME")
