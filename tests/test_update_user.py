import pytest
import allure
from data import TestData
from api_client import UserAPI
from helpers import generate_user_data, generate_unique_email   


class TestUpdateUser:

    @allure.title("Успешное изменение email авторизованного пользователя")
    @allure.description("Проверка успешного изменения email у авторизованного пользователя")
    def test_update_user_email_with_auth(self, create_and_delete_user):
        user_data, token = create_and_delete_user
        
        with allure.step("Генерация нового email"):
            new_email = generate_unique_email()  
            update_data = {"email": new_email}
            allure.attach(f"Новый email: {new_email}", name="Данные для обновления", 
                         attachment_type=allure.attachment_type.TEXT)
        
        with allure.step("Обновление email пользователя"):
            response = UserAPI.update_user(token, update_data)
        
        with allure.step("Проверка успешного обновления"):
            assert response.status_code == 200, \
                f"Ожидался 200, получен {response.status_code}. Ответ: {response.text}"
            response_data = response.json()
            assert response_data.get('success') is True, "success должно быть True"
            assert 'user' in response_data, "В ответе должен быть объект user"
            assert response_data['user']['email'] == new_email, \
                f"Email не обновился. Ожидался: {new_email}, Получен: {response_data['user']['email']}"
            allure.attach(f"Email успешно изменен на {new_email}", 
                         name="Результат", 
                         attachment_type=allure.attachment_type.TEXT)

    @allure.title("Успешное изменение пароля авторизованного пользователя")
    @allure.description("Проверка успешного изменения пароля у авторизованного пользователя")
    def test_update_user_password_with_auth(self, create_and_delete_user):
        user_data, token = create_and_delete_user
        
        with allure.step("Генерация нового пароля"):
            new_password = generate_user_data()['password']
            update_data = {"password": new_password}
            allure.attach(f"Новый пароль: {new_password}", name="Данные для обновления", 
                         attachment_type=allure.attachment_type.TEXT)
        
        with allure.step("Обновление пароля пользователя"):
            response = UserAPI.update_user(token, update_data)
        
        with allure.step("Проверка успешного обновления"):
            assert response.status_code == 200, \
                f"Ожидался 200, получен {response.status_code}. Ответ: {response.text}"
            response_data = response.json()
            assert response_data.get('success') is True, "success должно быть True"
            
            login_data = {
                "email": user_data['email'],
                "password": new_password
            }
            login_response = UserAPI.login_user(login_data)
            assert login_response.status_code == 200, \
                f"Не удалось залогиниться с новым паролем. Статус: {login_response.status_code}"
            allure.attach("Пароль успешно изменен", 
                         name="Результат", 
                         attachment_type=allure.attachment_type.TEXT)

    @allure.title("Успешное изменение имени авторизованного пользователя")
    @allure.description("Проверка успешного изменения имени у авторизованного пользователя")
    def test_update_user_name_with_auth(self, create_and_delete_user):
        user_data, token = create_and_delete_user
        
        with allure.step("Генерация нового имени"):
            new_name = generate_user_data()['name']
            update_data = {"name": new_name}
            allure.attach(f"Новое имя: {new_name}", name="Данные для обновления", 
                         attachment_type=allure.attachment_type.TEXT)
        
        with allure.step("Обновление имени пользователя"):
            response = UserAPI.update_user(token, update_data)
        
        with allure.step("Проверка успешного обновления"):
            assert response.status_code == 200, \
                f"Ожидался 200, получен {response.status_code}. Ответ: {response.text}"
            response_data = response.json()
            assert response_data.get('success') is True, "success должно быть True"
            assert 'user' in response_data, "В ответе должен быть объект user"
            assert response_data['user']['name'] == new_name, \
                f"Имя не обновилось. Ожидалось: {new_name}, Получено: {response_data['user']['name']}"
            allure.attach(f"Имя успешно изменено на {new_name}", 
                         name="Результат", 
                         attachment_type=allure.attachment_type.TEXT)

    @allure.title("Изменение данных пользователя без авторизации")
    @allure.description("Проверка ошибки при попытке изменить данные без токена авторизации")
    def test_update_user_without_auth(self):
        with allure.step("Генерация новых данных"):
            update_data = generate_user_data()
            allure.attach(f"Данные для обновления: {update_data}", 
                         name="Попытка обновления", 
                         attachment_type=allure.attachment_type.JSON)
        
        with allure.step("Попытка обновления данных без токена"):
            response = UserAPI.update_user_without_auth(update_data)
        
        with allure.step("Проверка ответа с ошибкой"):
            assert response.status_code == 401, \
                f"Ожидался 401, получен {response.status_code}. Ответ: {response.text}"
            response_data = response.json()
            assert response_data.get('success') is False, "success должно быть False"
            assert response_data.get('message') == TestData.ERROR_MESSAGES['unauthorized'], \
                f"Неверное сообщение об ошибке. Ожидалось: {TestData.ERROR_MESSAGES['unauthorized']}, Получено: {response_data.get('message')}"
            allure.attach(f"Ошибка: {response_data.get('message')}", 
                         name="Результат", 
                         attachment_type=allure.attachment_type.TEXT)

    @allure.title("Изменение данных пользователя с неверным токеном")
    @allure.description("Проверка ошибки при попытке изменить данные с неверным токеном")
    def test_update_user_invalid_token(self):
        invalid_token = "invalid_token_12345"
        update_data = generate_user_data()
        
        with allure.step("Попытка обновления данных с неверным токеном"):
            response = UserAPI.update_user(invalid_token, update_data)
        
        with allure.step("Проверка ответа с ошибкой"):
            assert response.status_code in [401, 403], \
                f"Ожидался 401 или 403, получен {response.status_code}. Ответ: {response.text}"
            response_data = response.json()
            assert response_data.get('success') is False, "success должно быть False"
            allure.attach(
                f"Статус: {response.status_code}, Сообщение: {response_data.get('message')}", 
                name="Результат", 
                attachment_type=allure.attachment_type.TEXT
            )

    @allure.title("Изменение нескольких полей одновременно")
    @allure.description("Проверка успешного изменения нескольких полей одновременно")
    def test_update_user_multiple_fields(self, create_and_delete_user):
        user_data, token = create_and_delete_user
        
        with allure.step("Генерация новых данных для обновления"):
            new_data = generate_user_data()
            unique_email = generate_unique_email()  
            update_data = {
                "email": unique_email,
                "name": new_data['name']
            }
            allure.attach(
                f"Новые данные: {update_data}", 
                name="Данные для обновления", 
                attachment_type=allure.attachment_type.JSON
            )
        
        with allure.step("Обновление нескольких полей пользователя"):
            response = UserAPI.update_user(token, update_data)
        
        with allure.step("Проверка успешного обновления"):
            assert response.status_code == 200, \
                f"Ожидался 200, получен {response.status_code}. Ответ: {response.text}"
            response_data = response.json()
            assert response_data.get('success') is True, "success должно быть True"
            assert 'user' in response_data, "В ответе должен быть объект user"
            user = response_data['user']
            assert user['email'] == update_data['email'], \
                f"Email не обновился. Ожидался: {update_data['email']}, Получен: {user['email']}"
            assert user['name'] == update_data['name'], \
                f"Имя не обновилось. Ожидалось: {update_data['name']}, Получено: {user['name']}"
            allure.attach(
                f"Email: {user['email']}, Имя: {user['name']}", 
                name="Обновленные данные", 
                attachment_type=allure.attachment_type.TEXT
            )