import jwt
import pytest
from mixer.backend.django import mixer

from app.auth.models import APIUser, TokenTypes
from app.auth.views import SignupView, LoginView, ChangePasswordView, SendResetPasswordEmailView, ResetPasswordView
from app.tests import get_json_request, get_json_response
from datetime import datetime

pytestmark = [pytest.mark.auth, pytest.mark.view, pytest.mark.django_db]


@pytest.mark.parametrize(
    'request_data,expected_status_code,expected_user_count',
    [
        ({'email': 'test@gmail.com', 'name': 'Name', 'password': 'password'}, 200, 1),
        ({'email': 'test@gmail.com', 'name': 'test'}, 422, 0),
        ({'email': 'test@gmail.com', 'name': 'Name', 'password': 'short'}, 422, 0),
    ],
    ids=[
        'correct signup form',
        'check that password is required',
        'check that user cannot sign up with short password',
    ],
)
def test_signup(request_data, expected_status_code, expected_user_count):
    request = get_json_request('post', data=request_data)
    response = get_json_response(SignupView, request)

    assert response.status_code == expected_status_code
    assert APIUser.objects.count() == expected_user_count
    if expected_status_code == 200:
        assert APIUser.objects.filter(email=request_data['email']).exists()


@pytest.mark.parametrize(
    'request_data,expected_status_code',
    [
        ({'email': 'test-user@2tapp.cc', 'password': 'Pa$$word'}, 200),
        ({'email': 'test-user@2tapp.cc', 'password': 'pa$$word'}, 400),
        ({'email': 'test-user@2tapp.cc'}, 422),
        ({'password': 'Pa$$word'}, 422),
    ],
    ids=[
        'password with correct register - OK',
        'password with incorrect register - NOT OK',
        'check that password is required',
        'check that email is required',
    ],
)
def test_login(request_data, expected_status_code):
    mixer.blend(APIUser, email='test-user@2tapp.cc', password=APIUser.make_password('Pa$$word'))
    mixer.blend(APIUser, email='test-user-2@2tapp.cc', password=APIUser.make_password('Pa$$word-2'))

    request = get_json_request('post', data=request_data)
    response = get_json_response(LoginView, request)

    assert response.status_code == expected_status_code
    if expected_status_code == 200:
        assert response.data['token']
        assert response.data['user']['email'] == request_data['email']


@pytest.mark.parametrize(
    'actions',
    [
        [
            {'view': SignupView, 'request_data': {'email': 'ExistingLower@2tapp.cc', 'password': 'Pa$$word'},
             'expected_status_code': 422},
            {'view': LoginView, 'request_data': {'email': 'ExistingLower@2tapp.cc', 'password': 'Pa$$word'},
             'expected_status_code': 200},
        ],
        [
            {'view': SignupView, 'request_data': {'email': 'New@2tapp.cc', 'password': 'Pa$$word'},
             'expected_status_code': 200},
            {'view': LoginView, 'request_data': {'email': 'new@2tapp.cc', 'password': 'Pa$$word'},
             'expected_status_code': 200},
        ],
        [
            {'view': SignupView, 'request_data': {'email': 'new@2tapp.cc', 'password': 'Pa$$word'},
             'expected_status_code': 200},
            {'view': LoginView, 'request_data': {'email': 'New@2tapp.cc', 'password': 'Pa$$word'},
             'expected_status_code': 200},
        ],
    ],
    ids=[
        'existing lower case email cannot sign up, but log in is working',
        'new mail is not lower, login is lower - OK',
        'new mail is lower, login is not lower - OK',
    ],
)
def test_case_sensitiveness(actions):
    mixer.blend(APIUser, email='existinglower@2tapp.cc', password=APIUser.make_password('Pa$$word'))

    for action_data in actions:
        view = action_data['view']
        request_data = action_data['request_data']
        expected_status_code = action_data['expected_status_code']

        request = get_json_request('post', data=request_data)
        response = get_json_response(view, request)

        assert response.status_code == expected_status_code

        if response.status_code == 422:
            assert response.data['errors'][0]['fields']['email'][
                       0] == 'The user with the provided email already exists.'

        if response.status_code == 200:
            expected_email = request_data['email'].lower()
            assert APIUser.objects.last().email == expected_email
            assert response.data['user']['email'] == expected_email


@pytest.mark.parametrize(
    'old_password,new_password,expected_status_code',
    [
        ('password', 'new_secret_password', 200),
        ('password', 'short', 422),
        ('incorrect_old_password', 'new_password', 422),
    ],
    ids=[
        'correct password change',
        'too short password',
        'old password is incorrect',
    ],
)
def test_change_password(registered_user, old_password, new_password, expected_status_code):
    request_data = {'old_password': old_password, 'new_password': new_password}
    request = get_json_request('post', data=request_data)
    request.user = registered_user

    response = get_json_response(ChangePasswordView, request)
    assert response.status_code == expected_status_code
    if expected_status_code == 200:
        assert APIUser.objects.get(email='registered@2tapp.cc').check_password(new_password)


@pytest.mark.parametrize(
    'request_data,expected_status_code',
    [
        ({'email': 'registered@2tapp.cc'}, 200),
        ({'email': 'notregistered@2tapp.cc'}, 200),
        ({'email': 'omg@this@mail is ++--- so # incorrect'}, 422),
        ({'message': 'forgot to add mail to request'}, 422),
    ],
    ids=[
        'registered mail able to change password',
        'say that email is sent even if user is not registered',
        'mail has to be correct',
        'mail is required',
    ],
)
def test_SendResetPasswordMail(registered_user, request_data, expected_status_code):
    request = get_json_request('post', data=request_data)
    response = get_json_response(SendResetPasswordEmailView, request)

    assert response.status_code == expected_status_code
    if response.status_code == 200:
        assert response.data['success'] is True


def test_ResetPasswordView(reset_password_fixture):
    token = reset_password_fixture['token']
    expected_status_code = reset_password_fixture['expected_status_code']
    password = 'new cool password'

    request_data = dict(
        token=token,
        password=password,
    )

    request = get_json_request('post', data=request_data)
    response = get_json_response(ResetPasswordView, request)

    assert response.status_code == expected_status_code
    if response.status_code == 200:
        assert response.data['success'] is True
    else:
        errors = response.data['errors']
        assert any(error['code'] == 'auth' for error in errors)
