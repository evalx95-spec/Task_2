import pytest
import allure
from data import TestData
from helpers import generate_user_data, generate_user_without_field
from api_client import UserAPI
from utils import extract_token


class TestUserCreation:

    @allure.title("Создание уникального пользователя")
    @allure.description("Проверка успешного создания нового уникального пользователя")
    def test_create_unique_user(self):
        
        with allure.step("Генерация данных пользователя"):
            user_data = generate_user_data()
        
        
        with allure.step("Отправка запроса на создание пользователя"):
            response = UserAPI.create_user(user_data)
        
       
        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 200, \
                f"Ожидался статус 200, получен {response.status_code}"
        
        with allure.step("Проверка данных созданного пользователя"):
            response_data = response.json()
            assert response_data.get('success') is True, "success должно быть True"
            
            user = response_data.get('user', {})
            assert user.get('email') == user_data['email'], \
                f"Email не совпадает"
            assert user.get('name') == user_data['name'], \
                f"Name не совпадает"
            
            assert 'accessToken' in response_data, "Отсутствует accessToken"
            assert 'refreshToken' in response_data, "Отсутствует refreshToken"
        
        
        with allure.step("Удаление созданного пользователя"):
            token = extract_token(response)
            if token:
                UserAPI.delete_user(token)

    @allure.title("Создание существующего пользователя")
    @allure.description("Проверка ошибки при попытке создать уже зарегистрированного пользователя")
    def test_create_existing_user(self, existing_user):
        user_data, _ = existing_user
        

        with allure.step("Попытка создать дубликат пользователя"):
            response = UserAPI.create_user(user_data)
        
        
        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 403, \
                f"Ожидался статус 403, получен {response.status_code}"
        
        with allure.step("Проверка тела ответа с ошибкой"):
            response_data = response.json()
            assert response_data.get('success') is False, "success должно быть False"
            assert response_data.get('message') == TestData.ERROR_MESSAGES['user_exists'], \
                f"Неверное сообщение об ошибке"

    @allure.title("Создание пользователя без обязательного поля")
    @allure.description("Проверка ошибки при попытке создать пользователя без одного из обязательных полей")
    @pytest.mark.parametrize("field_to_remove", ['email', 'password', 'name'])
    def test_create_user_without_field(self, field_to_remove):
        
        with allure.step(f"Генерация данных без поля '{field_to_remove}'"):
            user_data = generate_user_without_field(field_to_remove)
        
       
        with allure.step("Отправка запроса на создание пользователя"):
            response = UserAPI.create_user(user_data)
        
       
        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 403, \
                f"Ожидался статус 403, получен {response.status_code}"
        
        with allure.step("Проверка тела ответа с ошибкой"):
            response_data = response.json()
            assert response_data.get('success') is False, "success должно быть False"
            assert response_data.get('message') == TestData.ERROR_MESSAGES['missing_fields'], \
                f"Неверное сообщение об ошибке"
            assert 'accessToken' not in response_data, \
                "Пользователь не должен создаваться без обязательных полей"
