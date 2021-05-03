import pytest
from app.auth.models import APIUser


@pytest.fixture()
def registerme_user():
    user = APIUser.create_user('registerme@2tapp.cc', 'password')
    return user
