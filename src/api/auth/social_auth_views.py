import json
import requests
import jwt
from urllib.parse import parse_qs
from datetime import timedelta
from distutils import util

from django.utils import timezone
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import HttpRequest
from django.utils.translation import gettext as _

from ..utils.errors import error_response
from ..auth.models import APIUser
from .send_mails import send_email_registration
from .serializers import serialize_auth


class FacebookSignupView(View):
    def post(self, request):
        data = json.loads(request.body)
        token = data.get('token', None)

        if token:
            res = requests.get(
                url=settings.FACEBOOK_URL,
                params={
                    'fields': 'id, name, email',
                    'access_token': token
                }
            )

            if res.status_code == 400:
                return error_response('auth', _('invalid OAuth access token'))
            response_dict = res.json()
            email = response_dict.get('email', None)
            facebook_id = response_dict.get('id', None)
            name = response_dict.get('name', None)
            if facebook_id:
                already_exists = APIUser.objects.filter(facebook_id=facebook_id).count() > 0
                if already_exists:
                    user = APIUser.objects.get(facebook_id=facebook_id)
                    return JsonResponse(serialize_auth(user), status=200)
                user = APIUser.create_facebook_user(facebook_id, email=email, first_name=name)
                if user.email:
                    send_email_registration(user)
                return JsonResponse(serialize_auth(user), status=200)
            else:
                return error_response('auth', _('Empty facebook id'))
        else:
            error_response('auth', _('Facebook signup error'))


class AppleRedirectUrl(View):
    def get(self, request):
        params = {
            'client_id': settings.CLIENT_ID,
            'state': 'apple_login',
            'scope': 'email+name',
            'response_mode': 'form_post',
            'response_type': 'code',
            'redirect_uri': settings.REDIRECT_URI
        }
        url = 'https://appleid.apple.com/auth/authorize'
        return JsonResponse(data={'url': add_query_param(url, params)})


def add_query_param(url, params: dict):
    all_parapms = ""
    for key, value in params.items():
        all_parapms += key + '=' + value + '&'
    return url + '?' + all_parapms


def create_client_secret():
    secret_key = settings.APPLE_SECRET_TOKEN
    claims = {
        'iss': settings.APPLE_TEAM_ID,
        'aud': 'https://appleid.apple.com',
        'sub': settings.CLIENT_ID,
        'iat': timezone.now(),
        'exp': timezone.now() + timedelta(days=180)
    }
    headers = {'kid': settings.APPLE_KID, 'alg': 'ES256'}
    client_secret = jwt.encode(
        payload=claims,
        key=secret_key,
        algorithm='ES256',
        headers=headers
    ).decode('utf-8')
    return client_secret


class AppleSignupView(View):
    AUTH_URL = 'https://appleid.apple.com/auth/token'

    def post(self, request):
        body = request.body.decode('utf-8')
        data_body = parse_qs(body)
        code = data_body.get('code', None)[0]
        client_secret = create_client_secret()
        headers = {'content-type': "application/x-www-form-urlencoded"}
        data = {
            'client_id': settings.CLIENT_ID,
            'client_secret': client_secret,
            'code': code,
            'grant_type': 'authorization_code',
        }
        res = requests.post(AppleSignupView.AUTH_URL, data=data, headers=headers)
        response_dict = res.json()
        id_token = response_dict.get('id_token', None)
        User = get_user_model()
        if id_token:
            decoded = jwt.decode(id_token, '', verify=False)
            email = decoded['email']
            if email:
                already_exists = User.objects.filter(email=email).count() > 0
                if already_exists:
                    user = User.objects.get(email=email)
                    return JsonResponse(serialize_auth(user), status=200)
                user = User.objects.create_user(email, password=None, auth_provider=User.APPLE)
                return JsonResponse(serialize_auth(user), status=200)
            else:
                return error_response('auth', 'Not allowed require email')


class AppleIosSignupView(View):

    AUTH_URL = 'https://appleid.apple.com/auth/token'

    def post(self, request: HttpRequest):
        data = json.loads(request.body)
        code = data.get('code', None)
        if code:
            client_secret = create_client_secret()
            headers = {'content-type': "application/x-www-form-urlencoded"}
            data = {
                'client_id': settings.CLIENT_ID,
                'client_secret': client_secret,
                'code': code,
                'grant_type': 'authorization_code',
            }
            res = requests.post(AppleIosSignupView.AUTH_URL, data=data, headers=headers)
            response_dict = res.json()
            id_token = response_dict.get('id_token', None)
            if res.status_code == 200:
                decoded = jwt.decode(id_token, '', verify=False)
                email = decoded.get('email', None)
                sub = decoded.get('sub')
                fake_email = util.strtobool(decoded.get('is_private_email', 'false'))
                already_exists = APIUser.objects.filter(apple_id_sub=sub).count() > 0
                if already_exists:
                    user = APIUser.objects.get(apple_id_sub=sub)
                    return JsonResponse(serialize_auth(user), status=200)
                user = APIUser.create_apple_user(sub, email=email, fake_email=fake_email)
                if user.email:
                    send_email_registration(user)
                return JsonResponse(serialize_auth(user), status=200)
            else:
                return error_response('auth', str(response_dict))
        else:
            return error_response('auth', _('Apple signup error'))
