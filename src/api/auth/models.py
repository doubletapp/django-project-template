from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import (
    make_password, get_hasher
)
from django.utils.translation import gettext_lazy as _


class AdminUser(AbstractUser):
    pass


class APIUser(models.Model):
    first_name = models.CharField(max_length=64, blank=True, null=True, verbose_name=_('First name'))
    last_name = models.CharField(max_length=64, blank=True, null=True, verbose_name=_('Last name'))
    password = models.CharField(max_length=256, blank=True, null=True, verbose_name=_('Password'))
    email = models.EmailField(blank=True, null=True, verbose_name=_('Email'))
    fake_email = models.BooleanField(blank=True, null=True, verbose_name=_('Fake email'))
    apple_id_sub = models.CharField(max_length=128, blank=True, null=True, verbose_name=_('Apple ID sub'))
    facebook_id = models.CharField(max_length=64, blank=True, null=True, verbose_name=_('Facebook ID'))
    avatar = models.ImageField(upload_to='avatar', blank=True, null=True, verbose_name=_('Avatar'))

    class Meta:
        verbose_name = _('APIUser')
        verbose_name_plural = _('APIUsers')

    def __str__(self):
        return '{}:{}:{}'.format(self.email, self.first_name, self.last_name)

    @staticmethod
    def make_password(password, salt=None, hasher='default'):
        hasher = get_hasher(hasher)
        salt = salt or hasher.salt()
        return hasher.encode(password, salt)

    @staticmethod
    def create_apple_user(apple_id_sub, email=None, fake_email=None):
        return APIUser.objects.create(apple_id_sub=apple_id_sub, email=email, fake_email=fake_email)

    @staticmethod
    def create_facebook_user(facebook_id, email=None, first_name=None):
        return APIUser.objects.create(facebook_id=facebook_id, email=email, first_name=first_name)

    @staticmethod
    def create_email_user(email, password, name):
        return APIUser.objects.create(email=email, password=make_password(password), first_name=name)

