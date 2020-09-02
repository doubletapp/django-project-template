# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .auth.models import APIUser

admin.site.site_title = 'project_name administration'
admin.site.site_header = 'project_name administration'
admin.site.enable_nav_sidebar = False


admin.site.register(APIUser)

# Register your models here.
