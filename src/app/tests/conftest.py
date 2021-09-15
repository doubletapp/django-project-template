import jwt
import pytest
from app.auth.models import APIUser, TokenTypes
from datetime import datetime, timedelta

from config import settings


@pytest.fixture()
def registered_user():
    user = APIUser.create_user('registered@2tapp.cc', 'password')
    return user


REGISTERED = 'registered'
NOT_REGISTERED = 'not registered'
CORRECT = 'correct'
INCORRECT = 'incorrect'

token_params = [
    {
        'payload': {'type': CORRECT, 'datetime': datetime.now().isoformat(), 'id': REGISTERED},
        'key': CORRECT,
        'expected_status_code': 200
    },
    {
        'payload': {'type': INCORRECT, 'datetime': datetime.now().isoformat(), 'id': REGISTERED},
        'key': CORRECT,
        'expected_status_code': 400
    },
    {
        'payload': {'type': CORRECT, 'datetime': (datetime.now() - timedelta(days=2)).isoformat(), 'id': REGISTERED},
        'key': CORRECT,
        'expected_status_code': 400
    },
    {
        'payload': {'type': CORRECT, 'datetime': datetime.now().isoformat(), 'id': REGISTERED},
        'key': INCORRECT,
        'expected_status_code': 400
    },
    {
        'payload': {'type': CORRECT, 'datetime': datetime.now().isoformat(), 'id': NOT_REGISTERED},
        'key': CORRECT,
        'expected_status_code': 400
    },
]

token_ids = [
    'correct payload has to reset password',
    'check that type is correct',
    'check that token is fresh enough',
    'check token correctness',
    'cant reset password of not registered user',
]


@pytest.fixture(
    params=token_params,
    ids=token_ids,
)
def reset_password_fixture(request, registered_user):
    params = request.param

    payload = params['payload']
    key = settings.JWT_SECRET if params['key'] is CORRECT else 'incorrect key'
    expected_code = params['expected_status_code']

    payload['type'] = TokenTypes.reset_password.name if payload['type'] is CORRECT else 'incorrect type'
    payload['id'] = registered_user.id if payload['id'] is REGISTERED else -0xdeadbeef

    token = jwt.encode(payload, key, algorithm='HS256').decode()

    return dict(
        token=token,
        expected_status_code=expected_code
    )
