from django.core.mail import send_mail
from django.utils.translation import gettext as _

from .models import APIUser


def send_registration_email(user: APIUser):
    send_mail(
        _('Registration'),
        _('Seccessful registration in project_name'),
        None,
        [user.email],
    )
