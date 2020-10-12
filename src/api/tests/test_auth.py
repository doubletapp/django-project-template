import json
import urllib3
import requests
import responses

from django.urls.base import reverse
from django.test import TestCase, Client
from django.test import RequestFactory
from django.conf import settings

from ..auth.models import APIUser

client = Client()
HEADER = {'HTTP_SECRET': settings.API_SECRET}


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

