from pydantic import BaseModel

class UserResponse(BaseModel):
    email: str
    name: str
    age: int

    def __init__(self, user):
        super().__init__()
        self.email = user.email
        self.name = user.name
        self.age = user.age

class AuthResponse(BaseModel):
    token: str
    user: UserResponse
    
    def __init__(self, token, user):
        super().__init__()
        self.token = token
        self.user = UserResponse(user)


# from .models import APIUser


# def serialize_auth(user):
#     return dict(
#         token=user.get_auth_token(),
#         user=serialize_user(user),
#     )


# def serialize_user(user):
#     return dict(
#         id=user.id,
#         email=user.email,
#     )
