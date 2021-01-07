"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse

from api.auth.views import ResetPasswordFormHTMLView, ResetPasswordSuccessHTMLView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('reset_password_form', ResetPasswordFormHTMLView.as_view(), name='reset_password_form'),
    path('reset_password_success', ResetPasswordSuccessHTMLView.as_view(), name='reset_password_success'),
    path('metrics$', lambda request: HttpResponse('')),
]

handler500 = 'api.utils.errors.handler500'
handler400 = 'api.utils.errors.handler400'
handler404 = 'api.utils.errors.handler404'
handler403 = 'api.utils.errors.handler403'
