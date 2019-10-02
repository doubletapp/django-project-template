import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied


def is_api_call(request):
    return getattr(request, 'path').split('/')[1] == 'api'


class JWTAuthenticationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if is_api_call(request):
            try:
                authentication = request.headers['authentication']
                if not 'JWT ' in authentication:
                    raise Exception('invalid token')
                authentication = authentication.replace('JWT ', '')
                payload = jwt.decode(authentication, settings.JWT_SECRET, algorithms=['HS256'])
                user = get_user_model().objects.get(email=payload['email'])
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
            if not request.META.get('HTTP_SECRET') == settings.AUTH_SECRET:
                raise PermissionDenied

        response = self.get_response(request)
        return response
