from __future__ import unicode_literals
import json
import urllib3
import requests
import responses

from django.urls.base import reverse
from django.test import TestCase, Client
from django.test import RequestFactory
from django.conf import settings

from ..auth.social_auth_views import FacebookSignupView
from ..auth.models import APIUser

client = Client()
HEADER = {'HTTP_SECRET': settings.AUTH_SECRET}


class EmailSignUpTest(TestCase):
    def setUp(self):
        self.sign_up_url = reverse('signup')

        self.valid_payload = {
            'email': 'test@gmail.com',
            'name': 'Vasya',
            'password': 'password'
        }

        self.invalid_password = {
            'email': 'test@gmail.com',
            'name': 'test'
        }

    def test_sign_up_valid_payload(self):
        response = client.post(
            self.sign_up_url,
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            **HEADER
        )

        self.assertEqual(len(APIUser.objects.all()), 1)
        self.assertEqual(response.status_code, 200)

    def test_sign_up_invalid_pass(self):
        response = client.post(
            self.sign_up_url,
            data=json.dumps(self.invalid_password),
            content_type='application/json',
            **HEADER
        )
        answer = json.loads(response.content)
        correct_answer = {
            'errors':
                [
                    {'code': 'auth', 'message': 'Please enter email and password.'}
                ]
        }

        self.assertEqual(len(APIUser.objects.all()), 0)
        self.assertEqual(answer, correct_answer)
        self.assertEqual(response.status_code, 400)


class AppleIOSSignUpTest(TestCase):
    def setUp(self):
        self.apple_ios_url = reverse('apple_ios_signup')
        self.response_mock_obj = requests.Response

        self.valid_json_with_fake_mail = {
            'access_token': 'abeacc415466b41bab647080e13d3484d.0.mtvy.A0Ca-jsIvGI836YPgbQz8g',
            'token_type': 'Bearer',
            'expires_in': 3600,
            'refresh_token': 'r21e866e6e1b94f249ac06c375525cdf0.0.mtvy._CWTNqB6TKhXnNnVsfwbiA',
            'id_token': 'eyJraWQiOiI4NkQ4OEtmIiwiYWxnIjoiUlMyNTYifQ.eyJpc3MiOiJodHRwczovL2FwcGxlaWQuYXBwbGUuY29tIiwiYXVk'
                        'IjoibHUubWVkaXRhdGlvbi5hcHAuZG91YmxldGFwcC5kZXYiLCJleHAiOjE1ODIwMjQ2OTQsImlhdCI6MTU4MjAyNDA5NCw'
                        'ic3ViIjoiMDAwMzU4Ljg1ZjczNWRmMmRiMjRhYmE5MmUyYTM5YzliZjIwNWRjLjExNDIiLCJhdF9oYXNoIjoibUZGTUgycm'
                        'RwcWNJSzV2eFY3c2psZyIsImVtYWlsIjoic2o4OHd2czdjeUBwcml2YXRlcmVsYXkuYXBwbGVpZC5jb20iLCJlbWFpbF92Z'
                        'XJpZmllZCI6InRydWUiLCJpc19wcml2YXRlX2VtYWlsIjoidHJ1ZSIsImF1dGhfdGltZSI6MTU4MjAyNDA5MX0.Psx11Adr'
                        'Jto-tnT2TOhpxhce6qNGR3G0GmiXVt3v1oyCykoIhUE0i0koyJY0iTw9gd4WK3ch-Dz5JBIPGcuAHQMbYZGG_vqK8eIjgZw'
                        'wVTx3lkkvzHDv0PkxubhixFanRAtfuJ1mDzJSoUSjYRCiuCRRZqa6GM6WEDei7LLO9zN2yLWThE2EHiXFhNrN8K6JOY_Bfc'
                        '7F96sCX92a5oE3_wcDjHVbtwj3u2Vh5-MpvV4c_d30g4JohMBHPpXG3_9N9oVzO5oUYYvFNYyfPR5ssmZseShzJ-PLuDnnH'
                        'bzdOGSjZ1kbU8G4r3m-L_cfaktnb1KDNxIoPrkZ95QNosQI7A'}

        self.valid_json_with_mail = {
            'access_token': 'a2c960f5c11574c40b3479d8c80586142.0.mtvy.5FhS_o4bBMrhuABXvseaXQ',
            'token_type': 'Bearer',
            'expires_in': 3600,
            'refresh_token': 'r5bbbb90ccb58442290b5468c32a84ac9.0.mtvy.BV_jugDFowFRElvYBjEISg',
            'id_token': 'eyJraWQiOiI4NkQ4OEtmIiwiYWxnIjoiUlMyNTYifQ.eyJpc3MiOiJodHRwczovL2FwcGxlaWQuYXBwbGUuY29tIiwiYXVk'
                        'IjoibHUubWVkaXRhdGlvbi5hcHAuZG91YmxldGFwcC5kZXYiLCJleHAiOjE1ODIwMjc3ODIsImlhdCI6MTU4MjAyNzE4Miw'
                        'ic3ViIjoiMDAwMzU4Ljg1ZjczNWRmMmRiMjRhYmE5MmUyYTM5YzliZjIwNWRjLjExNDIiLCJhdF9oYXNoIjoiMVVPeG9HNS'
                        '1vSU1YN3ZKbnNQaVFZQSIsImVtYWlsIjoidGluZ2Fldi5tLnNAaWNsb3VkLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjoidHJ1Z'
                        'SIsImF1dGhfdGltZSI6MTU4MjAyNzE3OX0.ZrVKTYnijDuceIGYdLvrFqxKx_4E-xk5SMDpahN1gxMqDIySVxEa6aObWXMx'
                        'ha3yD7adLu30eBAwEmk8SLeqGlOdo-qhCRuNhySVj-lRhKxzubpUjhVrSb5njRvpJfylyGDMVDkuVBZ6sAcNWLmFhXa6ofg'
                        'Ud3EoTXb8QIuQ8Lp5Kq7JTRJmxemuiDLEe4nZVO5B5aP6co78BBY4eA_pmZr7EmWa-pQrPzt1mfF1oebDxsL23fawugCdDD'
                        'XLXPPa9sjFaLNuUiBBZgQ0Ym9gUp97EyYeqUE-QoE2JMzSWUJNyZrw1TUd6IorxZO3OYWZwStgXeiyvUp8MTaZMHd_cQ'}

    def test_with_fake_email(self):
        with responses.RequestsMock() as resp:
            resp.add(
                method=responses.POST,
                url='https://appleid.apple.com/auth/token',
                json=self.valid_json_with_fake_mail,
                status=200
            )
            header = {
                'HTTP_SECRET': settings.AUTH_SECRET
            }
            client.post(
                self.apple_ios_url,
                content_type='application/json',
                data={
                    'code':'398y64287rygufwhrfuy4ge'
                },
                **header
            )
            self.assertEqual(len(APIUser.objects.all()), 1)
            print(APIUser.objects.first())
            self.assertEqual(APIUser.objects.first().fake_email, True)
            self.assertEqual(APIUser.objects.first().apple_id_sub, '000358.85f735df2db24aba92e2a39c9bf205dc.1142')

    def test_with_mail(self):
        with responses.RequestsMock() as resp:
            resp.add(
                method=responses.POST,
                url='https://appleid.apple.com/auth/token',
                json=self.valid_json_with_mail,
                status=200
            )
            header = {
                'Code':'12432sdgwe3532erf423e3dasfq43rq3',
                'HTTP_SECRET': settings.AUTH_SECRET
            }
            client.post(
                self.apple_ios_url,
                content_type='application/json',
                data={
                    'code': '398y64287rygufwhrfuy4ge'
                },
                **header
            )
            self.assertEqual(len(APIUser.objects.all()), 1)
            print(APIUser.objects.first())
            self.assertEqual(APIUser.objects.first().fake_email, False)
            self.assertEqual(APIUser.objects.first().email, 'tingaev.m.s@icloud.com')
            self.assertEqual(APIUser.objects.first().apple_id_sub, '000358.85f735df2db24aba92e2a39c9bf205dc.1142')


class SignUpFacebookTest(TestCase):

    def setUp(self):
        self.signup_fb_url = reverse('signup_fb')
        self.request_factory = RequestFactory()

    def test_with_valid_data(self):
        http = urllib3.PoolManager()  # TODO: Meditation-4: Переделать на использование requests
        r = http.request('GET',
                         'https://graph.facebook.com/v5.0/app/accounts/test-users',
                         fields={
                             'fields': 'access_token',
                             'access_token': settings.FB_APP_TOKEN
                         })
        response_data = json.loads(r.data.decode('utf-8'))
        test_users = response_data.get('data', None)
        test_token = test_users[0]['access_token']

        signup_request = self.request_factory.post(self.signup_fb_url,
                                                   data=json.dumps({'token': '{}'.format(test_token)}),
                                                   content_type='application/json')
        signup_response = FacebookSignupView.as_view()(signup_request)
        self.assertEqual(signup_response.status_code, 200)

    def test_with_invalid_data(self):
        signup_request = self.request_factory.post(self.signup_fb_url,
                                                   data=json.dumps({'token': 'token'}),
                                                   content_type='application/json')
        signup_response = FacebookSignupView.as_view()(signup_request)
        print(type(signup_response))
        self.assertEqual(signup_response.status_code, 400)
