from pydantic import BaseModel

class PetResponse(BaseModel):
    name: str
    age: int
    age_str: str

    def __init__(self, pet):
        super().__init__()
        self.name = pet.name
        self.age = pet.age
        self.age_str = f'Возраст: {self.age}'

 
class PetListResponse(BaseModel):
    count: int
    items: PetResponse
    
    def __init__(self, pets, count):
        self.count = count
        self.items = [PetResponse(pet) for pet in pets]
