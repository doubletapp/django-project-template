from django.conf.urls import url

from .views import (
    LoginView,
    SignupView,
    ChangePasswordView,
    SendResetPasswordEmailView,
    ResetPassFormView
)

from .social_auth_views import (
    AppleIosSignupView,
    AppleSignupView,
    AppleRedirectUrl,
    FacebookSignupView
)


urlpatterns = [
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^signup/', SignupView.as_view(), name='signup'),
    url(r'^change_password/', ChangePasswordView.as_view()),
    url(r'^send_reset_password_email/', SendResetPasswordEmailView.as_view()),
    url(r'^reset_pass_form/', ResetPassFormView.as_view(), name='reset_pass_form'),

    url(r'^signup_fb/', FacebookSignupView.as_view(), name='signup_fb'),
    url(r'^apple_redirect_url/', AppleRedirectUrl.as_view(), name='apple_redirect_url'),
    url(r'^apple_ios_signup/', AppleIosSignupView.as_view(), name='apple_ios_signup'),
    url(r'^redirect_apple/', AppleSignupView.as_view(), name='signup_apple'),
]
