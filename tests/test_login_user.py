import pytest
import allure
from data import TestData
from api_client import UserAPI


class TestUserLogin:

    @allure.title("Логин существующего пользователя")
    @allure.description("Проверка успешного логина существующего пользователя")
    def test_login_existing_user(self, existing_user):
        user_data, _ = existing_user
        
        with allure.step("Подготовка учетных данных"):
            credentials = {
                "email": user_data['email'],
                "password": user_data['password']
            }
        
        with allure.step("Отправка запроса на логин"):
            response = UserAPI.login_user(credentials)
        
        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 200, \
                f"Ожидался статус 200, получен {response.status_code}"
        
        with allure.step("Проверка тела ответа"):
            response_data = response.json()
            assert response_data.get('success') is True, \
                "success должно быть True"
            assert 'accessToken' in response_data, \
                "Отсутствует accessToken"
            assert 'refreshToken' in response_data, \
                "Отсутствует refreshToken"
            assert 'user' in response_data, \
                "Отсутствует информация о пользователе"
        
        with allure.step("Проверка данных пользователя в ответе"):
            user = response_data.get('user')
            assert user.get('email') == user_data['email'], \
                f"Email не совпадает"
            assert user.get('name') == user_data['name'], \
                f"Name не совпадает"

    @allure.title("Логин с неверными учетными данными")
    @allure.description("Проверка ошибки при логине с неверным логином или паролем")
    @pytest.mark.parametrize("test_case", TestData.INVALID_LOGIN_CASES)
    def test_login_invalid_credentials(self, existing_user, test_case):
        user_data, _ = existing_user
        
        with allure.step("Отправка запроса на логин с неверными данными"):
            response = UserAPI.login_user(test_case)
        
        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 401, \
                f"Ожидался статус 401, получен {response.status_code}"
        
        with allure.step("Проверка тела ответа с ошибкой"):
            response_data = response.json()
            assert response_data.get('success') is False, \
                "success должно быть False"
            assert response_data.get('message') == TestData.ERROR_MESSAGES['invalid_credentials'], \
                f"Неверное сообщение об ошибке"
