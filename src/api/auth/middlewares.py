import jwt
from django.conf import settings
from api.auth.models import APIUser
from api.utils.errors import unauthorized_response
from api.auth.models import TokenTypes


def is_api_call(request):
    return getattr(request, 'path').split('/')[1] == 'api'


class JWTAuthenticationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if is_api_call(request):
            try:
                authorization = request.headers['authorization']
                if not 'Bearer ' in authorization:
                    raise Exception
                authorization = authorization.replace('Bearer ', '')

                payload = jwt.decode(authorization, settings.JWT_SECRET, algorithms=['HS256'])
                if payload['type'] != TokenTypes.authorization.name:
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
            if not request.META.get('HTTP_SECRET') == settings.API_SECRET:
                return unauthorized_response()

        response = self.get_response(request)
        return response
