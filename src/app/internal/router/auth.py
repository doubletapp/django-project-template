from django.urls import path

# from .views import (
#     LoginView,
#     SignupView,
#     ChangePasswordView,
#     SendResetPasswordEmailView,
#     ResetPasswordView,
# )


urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('signup', SignupView.as_view(), name='signup'),
    path('change_password', ChangePasswordView.as_view(), name='change_password'),
    path('send_reset_password_email', SendResetPasswordEmailView.as_view(), name='send_reset_password_email'),
    path('reset_password', ResetPasswordView.as_view(), name='reset_password'),
]
