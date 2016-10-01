from storages.backends.s3boto import S3BotoStorage


def MediaS3BotoStorage(): S3BotoStorage(location='media')


def StaticS3BotoStorage(): S3BotoStorage(location='static')
