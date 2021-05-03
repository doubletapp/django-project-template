import pytest
from mixer.backend.django import mixer
from app.auth.models import APIUser
from app.auth.views import SignupView, LoginView, ChangePasswordView
from app.tests import get_json_request, get_json_response

pytestmark = [pytest.mark.auth, pytest.mark.view, pytest.mark.django_db]


@pytest.mark.parametrize(
    'request_data,expected_status_code,expected_user_count',
    [
        ({'email': 'test@gmail.com', 'name': 'Name', 'password': 'password'}, 200, 1),
        ({'email': 'test@gmail.com', 'name': 'test'}, 422, 0),
        ({'email': 'test@gmail.com', 'name': 'Name', 'password': 'short'}, 422, 0),
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
            {'view': SignupView, 'request_data': {'email': 'ExistingLower@2tapp.cc', 'password': 'Pa$$word'}, 'expected_status_code': 422},
            {'view': LoginView, 'request_data': {'email': 'ExistingLower@2tapp.cc', 'password': 'Pa$$word'}, 'expected_status_code': 200},
        ],
        [
            {'view': SignupView, 'request_data': {'email': 'New@2tapp.cc', 'password': 'Pa$$word'}, 'expected_status_code': 200},
            {'view': LoginView, 'request_data': {'email': 'new@2tapp.cc', 'password': 'Pa$$word'}, 'expected_status_code': 200},
        ],
        [
            {'view': SignupView, 'request_data': {'email': 'new@2tapp.cc', 'password': 'Pa$$word'}, 'expected_status_code': 200},
            {'view': LoginView, 'request_data': {'email': 'New@2tapp.cc', 'password': 'Pa$$word'}, 'expected_status_code': 200},
        ],
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
            assert response.data['errors'][0]['fields']['email'][0] == 'The user with the provided email already exists.'

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
    ]
)
def test_change_password(registerme_user, old_password, new_password, expected_status_code):
    request_data = {'old_password': old_password, 'new_password': new_password}
    request = get_json_request('post', data=request_data)
    request.user = registerme_user

    response = get_json_response(ChangePasswordView, request)
    assert response.status_code == expected_status_code
    if expected_status_code == 200:
        assert APIUser.objects.get(email='registerme@2tapp.cc').check_password(new_password)


def test_mocker(mocker):
    mail = mocker.patch('django.core.mail.send_mail')
    mail.assert_not_called()
