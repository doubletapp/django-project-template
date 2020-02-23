import json
import jwt
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail
from django.core.exceptions import PermissionDenied

from api.utils.errors import error_response


def serialize_user(user):
    return dict(
        id=user.id,
        email=user.email,
    )

def serialize_auth(user):
    return dict(
        token=jwt.encode({'email': user.email}, settings.JWT_SECRET, algorithm='HS256').decode('utf-8'),
        user=serialize_user(user),
    )


class AuthenticatedView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user:
            raise PermissionDenied

        return super(AuthenticatedView, self).dispatch(request, *args, **kwargs)


class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data.get('email', '').lower().strip()
        password = data.get('password', None)

        if email and password:
            try:
                user = get_user_model().objects.get(email__iexact=email)
                if not user.check_password(password):
                    raise Exception('Incorrect password.')
                return JsonResponse(serialize_auth(user), status=200)
            except:
                return error_response('auth', 'Unable to login with the provided credentials.')
        else:
            return error_response('auth', 'Please enter email and password.')


class SignupView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data.get('email', '').lower().strip()
        password = data.get('password', None)

        if email and password:
            already_exists = get_user_model().objects.filter(email__iexact=email).count() > 0
            if already_exists:
                return error_response('auth', 'A user with this email already exists.')

            user = get_user_model().objects.create_user(email, password)
            return JsonResponse(serialize_auth(user), status=200)
        else:
            return error_response('auth', 'Please enter email and password.')


class ChangePasswordView(AuthenticatedView):
    def post(self, request):
        data = json.loads(request.body)
        old_password = data.get('old_password', '').strip()
        new_password = data.get('new_password', '').strip()
        user = request.user

        if old_password and new_password:
            if not user.check_password(old_password):
                return error_response('auth', 'Incorrect old password.')

            user.set_password(new_password)
            user.save()

            return JsonResponse({
                'success': True
            }, status=200)
        else:
            return error_response('auth', 'Please enter old password and new password.')


class SendResetPasswordEmailView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data.get('email', '').lower().strip()
        if not email:
            return error_response('auth', 'Please enter email.')

        try:
            user = get_user_model().objects.get(email=email)
            token = jwt.encode({
                'email': user.email,
                'created_at': datetime.now().timestamp(),
            }, settings.JWT_SECRET, algorithm='HS256').decode('utf-8')
            send_mail(
                'Reset password',
                f'Token: {token}',
                None,
                [email],
            )
        except:
            pass

        return JsonResponse({
            'success': True
        }, status=200)


class ResetPasswordView(View):
    def post(self, request):
        data = json.loads(request.body)
        token = data.get('token', None)
        new_password = data.get('new_password', '').strip()

        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
            created_at = datetime.fromtimestamp(payload['created_at'])
            created_from_now = datetime.now() - created_at
            if created_from_now > timedelta(hours=24):
                raise Exception('Outdated.')
        except:
            return error_response('auth', 'Token is incorrect.')

        user = get_user_model().objects.get(email=payload['email'])
        user.set_password(new_password)
        user.save()

        return JsonResponse({
            'success': True
        }, status=200)
