from django.urls import path

from app.internal.transport.rest.pets.handlers import PetsHandler
from app.internal.service.pets import PetService


urlpatterns = [
    path('pets', PetsHandler.as_view(), name='pets'),
    # path('happy_pets', LoginView.as_view(), name='happy-pets'),
]
