from django.conf.urls import url
from django.urls import include

from api.auth.views import LoginView, SignupView, ChangePasswordView, SendResetPasswordEmailView, ResetPasswordView

urlpatterns = [
    url(r'^login/', LoginView.as_view()),
    url(r'^signup/', SignupView.as_view()),
    url(r'^change_password/', ChangePasswordView.as_view()),
    url(r'^send_reset_password_email/', SendResetPasswordEmailView.as_view()),
    url(r'^reset_password/', ResetPasswordView.as_view()),
]
