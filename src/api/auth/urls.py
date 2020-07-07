from django.urls import path

from .views import (
    LoginView,
    SignupView,
    ChangePasswordView,
    SendResetPasswordEmailView,
    ResetPassFormView
)


urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('signup', SignupView.as_view(), name='signup'),
    path('change_password', ChangePasswordView.as_view()),
    path('send_reset_password_email', SendResetPasswordEmailView.as_view()),
    path('reset_pass_form', ResetPassFormView.as_view(), name='reset_pass_form'),
]
