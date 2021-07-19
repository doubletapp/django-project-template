from django.urls import include, path


urlpatterns = [
    path('auth/', include('app.internal.router.auth')),
    path('pets/', include('app.internal.router.pets')),

]
