from django.core.mail import send_mail
from django.utils.translation import gettext as _
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import APIUser


def send_email_registration(user: APIUser):
    # from_email=None if you set DEFAULT_FROM_EMAIL in .env file
    from_email, to = None, [
        user.email,
    ]
    html_subject = render_to_string('mailbox/email_confirmation_subject.html', {'context': 'values'})
    plain_subject = strip_tags(html_subject)
    html_message = render_to_string('mailbox/email_confirmation_message.html', {'context': 'values'})
    plain_message = strip_tags(html_message)

    send_mail(_(plain_subject), _(plain_message), from_email, to, html_message=html_message)

    print('Email of registration sent')
