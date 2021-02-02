from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import ModelForm, PasswordInput
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from django.conf import settings

from .auth.models import AdminUser, APIUser


admin.site.site_title = 'project_name'
admin.site.site_header = 'project_name'
admin.site.enable_nav_sidebar = False


@admin.register(AdminUser)
class AdminUserAdmin(UserAdmin):
    pass


class APIUserForm(ModelForm):
    def clean_password(self):
        cleaned_data = super(APIUserForm, self).clean()
        password = cleaned_data.get('password')

        if len(password) < settings.PASSWORD_MIN_LENGTH:
            raise ValidationError("The password must be at least 8 characters long.")

        if password != self.instance.password:
            password = APIUser.make_password(password)

        return password

    class Meta:
        model = APIUser
        exclude = ()
        widgets = {
            'password': PasswordInput(render_value=True),
        }


@admin.register(APIUser)
class APIUserAdmin(admin.ModelAdmin):
    form = APIUserForm
    list_display = ('email',)
