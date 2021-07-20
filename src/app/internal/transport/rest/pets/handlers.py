from django.http import response
from app.pkg.handler import Handler

from app.internal.transport.http.pets.responses import PetListResponse
from app.internal.transport.http.pets.requests import PetListRequest
from app.internal.service.pets import PetService

class PetsHandler(Handler):
    @handle(request=PetListRequest, response=PetListResponse, )
    def get(self, request):
        pets_service = PetService()
        
        return pets_service.get_pets()

