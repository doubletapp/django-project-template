from django import forms


class NewPasswordForm(forms.Form):
    password = forms.PasswordInput()
    password_confirm = forms.PasswordInput()
