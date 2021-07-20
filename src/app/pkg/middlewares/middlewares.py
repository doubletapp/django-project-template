import jwt
from django.conf import settings
from app.auth.models import APIUser
from app.utils.errors import unauthorized_response
from app.auth.models import TokenTypes
from app.logging import log


def is_api_call(request):
    return getattr(request, 'path').split('/')[1] == 'api'


class JWTAuthenticationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if is_api_call(request):
            try:
                authorization = request.headers.get('authorization')
                if not authorization:
                    raise Exception
                if not 'Bearer ' in authorization:
                    log.debug('no "Bearer " in authorization header')
                    raise Exception
                authorization = authorization.replace('Bearer ', '')

                payload = jwt.decode(authorization, settings.JWT_SECRET, algorithms=['HS256'])
                if payload['type'] != TokenTypes.authorization.name:
                    log.debug('incorrect token type')
                    raise Exception

                user = APIUser.objects.get(id=payload['id'])
                request.user = user
            except:
                request.user = None

        response = self.get_response(request)
        return response


class SecretAuthenticationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if is_api_call(request):
            secret = request.META.get('HTTP_SECRET')
            if not secret == settings.API_SECRET:
                if secret:
                    log.debug('incorrect secret')
                return unauthorized_response()

        response = self.get_response(request)
        return response
