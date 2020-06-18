from django.conf.urls import url

from .views import (
    LoginView,
    SignupView,
    ChangePasswordView,
    SendResetPasswordEmailView,
    ResetPassFormView
)


urlpatterns = [
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^signup/', SignupView.as_view(), name='signup'),
    url(r'^change_password/', ChangePasswordView.as_view()),
    url(r'^send_reset_password_email/', SendResetPasswordEmailView.as_view()),
    url(r'^reset_pass_form/', ResetPassFormView.as_view(), name='reset_pass_form'),
]
