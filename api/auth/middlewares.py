import jwt
from django.conf import settings
from django.contrib.auth import get_user_model

class JWTAuthenticationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            authentication = request.headers['authentication'].replace('JWT', '').replace(' ', '')
            payload = jwt.decode(authentication, settings.SECRET_KEY, algorithms=['HS256'])
            user = get_user_model().objects.get(email=payload['email'])
            request.user = user
        except:
            pass

        response = self.get_response(request)
        return response
