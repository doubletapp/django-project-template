from django.test import tag, TestCase
from http import HTTPStatus
from django.conf import settings
import boto3


# class TestStorage(TestCase):
#     @tag('storage')
#     def test_get_file_from_buket_200(self):
#         session = boto3.session.Session()
#         s3 = session.client(
#             service_name='s3'
#             # default use Amazon
#             # endpoint_url = 'https://storage.yandexcloud.net'
#         )

#         key = f'autotest/{settings.ENVIRONMENT}'
#         bucket = settings.AWS_STORAGE_BUCKET_NAME
#         get_object_respose = s3.get_object(Bucket=bucket, Key=key)
#         self.assertEqual(get_object_respose['ResponseMetadata']['HTTPStatusCode'], HTTPStatus.OK)
