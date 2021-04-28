import jwt
from datetime import datetime
from enum import Enum

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password, get_hasher
from django.contrib.auth.hashers import check_password
from django.utils.translation import gettext_lazy as _


class TokenTypes(Enum):
    authorization = 'authorization'
    reset_password = 'reset_password'


class AdminUser(AbstractUser):
    pass


class APIUser(models.Model):
    email = models.EmailField(unique=True, verbose_name=_('Email'))
    password = models.CharField(max_length=255, verbose_name=_('Password'))
    avatar = models.ImageField(null=True)

    class Meta:
        verbose_name = _('APIUser')
        verbose_name_plural = _('APIUsers')

    def __str__(self):
        return self.email

    @staticmethod
    def create_user(email, password):
        return APIUser.objects.create(email=email, password=make_password(password))

    @staticmethod
    def make_password(password, salt=None, hasher='default'):
        hasher = get_hasher(hasher)
        salt = salt or hasher.salt()
        return hasher.encode(password, salt)

    def _get_token(self, type):
        now = datetime.now().isoformat()
        return jwt.encode(
            dict(
                type=type,
                id=self.id,
                datetime=now,
            ),
            settings.JWT_SECRET,
            algorithm='HS256',
        ).decode('utf-8')

    def get_auth_token(self):
        return self._get_token(TokenTypes.authorization.name)

    def get_reset_password_token(self):
        return self._get_token(TokenTypes.reset_password.name)

    def check_password(self, password):
        return check_password(password, self.password)
