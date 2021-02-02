from .models import APIUser


def serialize_auth(user):
    return dict(
        token=user.get_auth_token(),
        user=serialize_user(user),
    )


def serialize_user(user):
    return dict(
        id=user.id,
        email=user.email,
    )
