import pytest
from app.auth.models import APIUser


@pytest.fixture()
def registered_user():
    user = APIUser.create_user('registered@2tapp.cc', 'password')
    return user
