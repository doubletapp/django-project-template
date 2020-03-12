from django.core.mail import send_mail
from django.utils.translation import gettext as _

from .models import APIUser


def send_email_registration(user: APIUser):
    send_mail(
        _('Registration'),
        _('Seccessful registration in Luapp: Meditation and Slepp'),
        None,
        [user.email],
    )
