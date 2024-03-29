import json
from datetime import datetime, timedelta

import jwt
import requests
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.urls.base import reverse
from django.utils.translation import gettext as _
from django.views import View

from app.utils.decorators import validate_form
from app.utils.errors import error_response, unauthorized_response
from app.utils.urls import get_absolute_url
from .emails import send_registration_email
from .forms import SignUpForm, LoginForm, ChangePasswordForm, SendResetPasswordEmailForm, ResetPasswordForm
from .models import APIUser, TokenTypes
from .serializers import serialize_auth


class AuthenticatedView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user:
            return unauthorized_response()

        return super(AuthenticatedView, self).dispatch(request, *args, **kwargs)


class LoginView(View):
    @validate_form(LoginForm)
    def post(self, request, form_data):
        email = form_data['email']
        password = form_data['password']

        try:
            user = APIUser.objects.get(email=email)
            if user.check_password(password):
                return JsonResponse(serialize_auth(user), status=200)

            raise APIUser.DoesNotExist
        except APIUser.DoesNotExist:
            return error_response('auth', _('Unable to login with the provided credentials'))


class SignupView(View):
    @validate_form(SignUpForm)
    def post(self, request, form_data):
        email = form_data['email']
        password = form_data['password']

        user = APIUser.create_user(email, password)
        send_registration_email(user)

        return JsonResponse(serialize_auth(user))


class ChangePasswordView(AuthenticatedView):
    @validate_form(ChangePasswordForm)
    def post(self, request, form_data):
        user = request.user
        new_password = form_data['new_password']
        user.password = user.make_password(new_password)
        user.save()

        return JsonResponse({'success': True}, status=200)


class SendResetPasswordEmailView(View):
    @validate_form(SendResetPasswordEmailForm)
    def post(self, request, form_data):
        email = form_data['email']

        try:
            user = APIUser.objects.get(email=email)
            token = user.get_reset_password_token()
            reset_password_path = reverse('reset_password_form') + f'?token={token}'
            url = get_absolute_url(request, reset_password_path)

            send_mail(
                'Reset password',
                f'Rest password URL: {url}',
                None,
                [email],
            )
        except APIUser.DoesNotExist:
            pass

        return JsonResponse({'success': True}, status=200)


class ResetPasswordView(View):
    @validate_form(ResetPasswordForm)
    def post(self, request, form_data):
        token = form_data['token']
        password = form_data['password']

        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
            if payload['type'] != TokenTypes.reset_password.name:
                raise Exception()

            token_life_time = datetime.now() - datetime.fromisoformat(payload['datetime'])
            if token_life_time > timedelta(hours=24):
                raise Exception()

            user = APIUser.objects.get(id=payload['id'])
            user.password = APIUser.make_password(password)
            user.save()
        except:
            return error_response('auth', 'Password reset link is incorrect or outdated.')

        return JsonResponse({'success': True}, status=200)


class ResetPasswordFormHTMLView(View):
    def get(self, request):
        return render(request, 'reset_password_form.html')

    def post(self, request):
        data = dict(
            token=request.GET.get('token'),
            password=request.POST.get('password'),
        )

        headers = {'content-type': 'application/json', 'secret': settings.API_SECRET}
        response = requests.post(url=get_absolute_url(request, reverse('reset_password')), json=data, headers=headers)

        if response.ok:
            return redirect(reverse('reset_password_success'))

        response_body = json.loads(response.text)
        context = dict(error=response_body['errors'][0]['message'])
        template = loader.get_template('reset_password_form.html')
        return HttpResponse(template.render(context, request))


class ResetPasswordSuccessHTMLView(View):
    def get(self, request):
        return render(request, 'reset_password_success.html')
