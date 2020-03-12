# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .auth.models import APIUser

admin.site.register(APIUser)

# Register your models here.
