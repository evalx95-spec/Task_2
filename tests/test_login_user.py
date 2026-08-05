import pytest
import allure
from ..data import TestData
from ..helpers import UserHelper

class TestUserLogin:

    @allure.title("Логин существующего пользователя")
    @allure.description("Проверка успешного логина существующего пользователя")
    def test_login_existing_user(self):
        user_data = TestData.EXISTING_USER.copy()
        UserHelper.create_user(user_data)

        credentials = {
            "email": user_data['email'],
            "password": user_data['password']
        }
        response = UserHelper.login_user(credentials)

        assert response.status_code == 200

        response_data = response.json()
        assert response_data.get('success') is True
        assert 'accessToken' in response_data
        assert 'refreshToken' in response_data
        assert 'user' in response_data

        user = response_data.get('user')
        assert user.get('email') == user_data['email']
        assert user.get('name') == user_data['name']

    @allure.title("Логин с неверными учетными данными")
    @allure.description("Проверка ошибки при логине с неверным логином или паролем")
    @pytest.mark.parametrize("test_case", TestData.INVALID_LOGIN_CASES)
    def test_login_invalid_credentials(self, test_case):
        user_data = TestData.EXISTING_USER.copy()
        UserHelper.create_user(user_data)
        response = UserHelper.login_user(test_case)

        assert response.status_code == 401

        response_data = response.json()
        assert response_data.get('success') is False
        assert response_data.get('message') == TestData.ERROR_MESSAGES['invalid_credentials']
        