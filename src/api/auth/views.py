import json
import jwt
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseForbidden


class AuthenticatedView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user:
            return HttpResponseForbidden()

        return super(AuthenticatedView, self).dispatch(request, *args, **kwargs)


class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data.get('email', None)
        password = data.get('password', None)

        if email and password:
            try:
                user = get_user_model().objects.get(email=email)
                if not user.check_password(password):
                    raise Exception('Incorrect password.')
                return JsonResponse({
                    'token': jwt.encode({'email': user.email}, settings.JWT_SECRET, algorithm='HS256').decode('utf-8')
                }, status=200)
            except:
                return JsonResponse({
                    'errors': ['Unable to login with the provided credentials.']
                }, status=400)
        else:
            return JsonResponse({
                'errors': ['Please enter email and password.']
            }, status=400)


class SignupView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data.get('email', None)
        password = data.get('password', None)

        if email and password:
            already_exists = get_user_model().objects.filter(email=email).count() > 0
            if already_exists:
                return JsonResponse({
                    'errors': ['A user with this email already exists.']
                }, status=400)

            user = get_user_model().objects.create_user(email, password)
            return JsonResponse({
                'token': jwt.encode({'email': user.email}, settings.JWT_SECRET, algorithm='HS256').decode('utf-8')
            }, status=200)
        else:
            return JsonResponse({
                'errors': ['Please enter email and password.']
            }, status=400)


class ChangePasswordView(AuthenticatedView):
    def post(self, request):
        data = json.loads(request.body)
        old_password = data.get('old_password', None)
        new_password = data.get('new_password', None)
        user = request.user

        if old_password and new_password:
            if not user.check_password(old_password):
                return JsonResponse({
                    'errors': ['Incorrect old password.']
                }, status=400)

            user.set_password(new_password)
            user.save()

            return JsonResponse({
                'success': True
            }, status=200)
        else:
            return JsonResponse({
                'errors': ['Please enter old password and new password.']
            }, status=400)


class SendResetPasswordEmailView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data.get('email', None)
        if not email:
            return JsonResponse({
                'errors': ['Please enter email.']
            }, status=400)

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
        new_password = data.get('new_password', None)

        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
            created_at = datetime.fromtimestamp(payload['created_at'])
            created_from_now = datetime.now() - created_at
            if created_from_now > timedelta(hours=24):
                raise Exception('Outdated.')
        except:
            return JsonResponse({
                'errors': ['Token is incorrect.']
            }, status=400)

        user = get_user_model().objects.get(email=payload['email'])
        user.set_password(new_password)
        user.save()

        return JsonResponse({
            'success': True
        }, status=200)
