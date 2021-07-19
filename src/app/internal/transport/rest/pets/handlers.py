from django.http import response
from app.pkg.handler import Handler

from app.internal.transport.http.pets.responses import PetResponse
from app.internal.transport.http.pets.requests import PetRequest
from app.internal.service.pets import PetService

class PetsHandler(Handler):
    @handle(request=PetRequest, response=PetResponse, )
    def get(self, request):
        pets_service = PetService()
        pets = pets_service.get_pets()
        
        return pets

