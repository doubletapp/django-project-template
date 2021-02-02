from django.urls import include, path


urlpatterns = [
    path('auth/', include('app.auth.urls')),
]
