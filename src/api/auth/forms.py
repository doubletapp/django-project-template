from django import forms
from django.utils.translation import gettext as _

from .models import APIUser
from api.forms import Form


class SignUpForm(Form):    
    email = forms.EmailField()
    password = forms.CharField()

    def clean_email(self):
        email = self.cleaned_data['email']
        email = email.lower().strip()

        if APIUser.objects.filter(email=email).exists():
            raise forms.ValidationError(_('The user with the provided email already exists.'))

        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        password = password.strip()
        return password


class LoginForm(Form):
    email = forms.EmailField()
    password = forms.CharField()

    def clean_email(self):
        email = self.cleaned_data['email']
        email = email.lower().strip()
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        password = password.strip()
        return password


class ChangePasswordForm(Form):
    old_password = forms.CharField()
    new_password = forms.CharField()

    def clean_old_password(self):
        old_password = self.cleaned_data['old_password']
        if not self.request.user.check_password(old_password):
            raise forms.ValidationError(_('Incorrect password.'))
        return old_password


class SendResetPasswordEmailForm(Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data['email']
        email = email.lower().strip()

        return email


class ResetPasswordForm(Form):
    token = forms.CharField()
    password = forms.CharField()
