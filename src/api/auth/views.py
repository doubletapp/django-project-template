import json
import jwt
from datetime import datetime, timedelta

from django.http import JsonResponse
from django.views import View
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpRequest
from django.urls.base import reverse
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.core.exceptions import PermissionDenied

from api.utils.errors import error_response, not_valid_response, unauthorized_response
from .models import APIUser
from .forms import NewPasswordForm, SignUpForm, LoginForm, ChangePasswordForm
from .serializers import serialize_auth
from .emails import send_registration_email


class AuthenticatedView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user:
            return unauthorized_response()

        return super(AuthenticatedView, self).dispatch(request, *args, **kwargs)


class LoginView(View):
    def post(self, request):
        data = json.loads(request.body or '{}')
        form = LoginForm(data)

        if not form.is_valid():
            return not_valid_response(form.errors)

        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        try:
            user = APIUser.objects.get(email=email)
            if user.check_password(password):
                return JsonResponse(serialize_auth(user), status=200)

            raise APIUser.DoesNotExist
        except APIUser.DoesNotExist:
            return error_response('auth', _('Unable to login with the provided credentials'))


class SignupView(View):
    def post(self, request):
        data = json.loads(request.body or '{}')
        form = SignUpForm(data)

        if not form.is_valid():
            return not_valid_response(form.errors)

        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        user = APIUser.create_user(email, password)
        send_registration_email(user)

        return JsonResponse(serialize_auth(user))


class ChangePasswordView(AuthenticatedView):
    def post(self, request):
        user = request.user
        data = json.loads(request.body or '{}')
        form = ChangePasswordForm(data, request=request)

        if not form.is_valid():
            return not_valid_response(form.errors)

        new_password = form.cleaned_data['new_password']
        user.password = user.make_password(new_password)
        user.save()

        return JsonResponse({
            'success': True
        }, status=200)


class SendResetPasswordEmailView(View):
    def post(self, request: HttpRequest):
        data = json.loads(request.body)
        email = data.get('email', '').lower()

        if not email:
            return error_response('auth', _('Please enter email'))

        try:
            already_exists = APIUser.objects.get(email=email)

            if already_exists:
                user = APIUser.objects.get(email=email)
                token = jwt.encode({
                    'email': user.email,
                    'created_at': datetime.now().timestamp(),
                }, settings.JWT_SECRET, algorithm='HS256').decode('utf-8')
                link = '{}://{}{}'.format(
                    request.scheme,
                    request.get_host(),
                    reverse('reset_pass_form') + "?token={}".format(token))

                send_mail(
                    'Reset password',
                    f'Link: {link}',
                    None,
                    [email],
                )
            else:
                return error_response('auth', _('Not found user with this email'))
        except:
            pass

        return JsonResponse({
            'success': True
        }, status=200)


class ResetPassFormView(View):
    def get(self, request: HttpRequest):
        password_form = NewPasswordForm()
        return render(request, 'auth/passform.html', context={'form': password_form})

    def post(self, request: HttpRequest):
        token = request.GET.get('token', None)
        password_form = NewPasswordForm(request.POST)

        if password_form.is_valid():
            try:
                data = request.POST.dict()
                new_password = data['password']

                if data['password'] != data['password_confirm']:
                    return error_response('auth', _('Passwords do not match'))

                payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
                created_at = datetime.fromtimestamp(payload['created_at'])
                created_from_now = datetime.now() - created_at

                if created_from_now > timedelta(hours=24):
                    return error_response('auth', _('Time has expired'))
            except:
                return error_response('auth', _('Token is incorrect'))

        user = get_user_model().objects.get(email=payload['email'])
        user.set_password(new_password)
        user.save()

        return render(request, template_name='auth/done_pass.html')
