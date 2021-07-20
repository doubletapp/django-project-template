from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str


# from django import forms
# from django.utils.translation import gettext as _
# from django.conf import settings

# from app.forms import Form
# from app.auth.models import APIUser


# class SignUpForm(Form):
#     email = forms.EmailField()
#     password = forms.CharField()

#     def clean_email(self):
#         email = self.cleaned_data['email'].lower().strip()

#         if APIUser.objects.filter(email=email).exists():
#             raise forms.ValidationError(_('The user with the provided email already exists.'))

#         return email

#     def clean_password(self):
#         password = self.cleaned_data['password']
#         password = password.strip()

#         if len(password) < settings.PASSWORD_MIN_LENGTH:
#             raise forms.ValidationError(_('The password must be at least 8 characters long.'))

#         return password


# class LoginForm(Form):
#     email = forms.EmailField()
#     password = forms.CharField()

#     def clean_email(self):
#         return self.cleaned_data['email'].lower().strip()

#     def clean_password(self):
#         password = self.cleaned_data['password']
#         password = password.strip()
#         return password


# class ChangePasswordForm(Form):
#     old_password = forms.CharField()
#     new_password = forms.CharField()

#     def clean_old_password(self):
#         old_password = self.cleaned_data['old_password']

#         if not self.request.user.check_password(old_password):
#             raise forms.ValidationError(_('Incorrect password.'))

#         return old_password

#     def clean_new_password(self):
#         password = self.cleaned_data['new_password']
#         password = password.strip()

#         if len(password) < settings.PASSWORD_MIN_LENGTH:
#             raise forms.ValidationError(_('The password must be at least 8 characters long.'))

#         return password


# class SendResetPasswordEmailForm(Form):
#     email = forms.EmailField()

#     def clean_email(self):
#         return self.cleaned_data['email'].lower().strip()


# class ResetPasswordForm(Form):
#     token = forms.CharField()
#     password = forms.CharField()
