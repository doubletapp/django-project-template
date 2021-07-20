from django.apps import AppConfig as DefaultAppConfig


class AppConfig(DefaultAppConfig):
    name = 'app'


default_app_config = 'app.AppConfig'
