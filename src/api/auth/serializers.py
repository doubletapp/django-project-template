import jwt

from django.conf import settings

from .models import APIUser


def serialize_auth(user: APIUser):
    return dict(
        token=jwt.encode({'id': user.pk}, settings.JWT_SECRET, algorithm='HS256').decode('utf-8'),
        user=serialize_user(user),
    )


def serialize_user(user: APIUser):
    return dict(
        id=user.pk,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        fake_email=user.fake_email,
        apple_id_sub=user.apple_id_sub,
        facebook_id=user.facebook_id,
        avatar=user.avatar.url if user.avatar else None
    )
