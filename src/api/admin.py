from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .auth.models import AdminUser, APIUser


admin.site.site_title = 'project_name'
admin.site.site_header = 'project_name'
admin.site.enable_nav_sidebar = False


@admin.register(AdminUser)
class AdminUserAdmin(UserAdmin):
    pass


@admin.register(APIUser)
class APIUserAdmin(admin.ModelAdmin):
    pass
