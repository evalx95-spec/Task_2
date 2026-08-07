import requests
import allure
from faker import Faker
from urls import BASE_URL, ENDPOINTS

fake = Faker()


def generate_user_data():
    """Генерация случайных данных пользователя"""
    return {
        "email": fake.email(),
        "password": fake.password(length=8),
        "name": fake.first_name()
    }


def generate_user_without_field(field_to_remove):
    """Генерация данных пользователя без указанного поля"""
    user_data = generate_user_data()
    if field_to_remove in user_data:
        del user_data[field_to_remove]
    return user_data


class UserDataGenerator:
    """Класс для генерации тестовых данных пользователя"""
    
    @staticmethod
    def generate_user_data():
        return generate_user_data()
    
    @staticmethod
    def generate_user_without_field(field_to_remove):
        return generate_user_without_field(field_to_remove)


class UserHelper:

    @staticmethod
    @allure.step("Создание нового пользователя")
    def create_user(user_data):
        url = f"{BASE_URL}{ENDPOINTS['create_user']}"
        response = requests.post(url, json=user_data)
        return response

    @staticmethod
    @allure.step("Авторизация пользователя")
    def login_user(credentials):
        url = f"{BASE_URL}{ENDPOINTS['login_user']}"
        response = requests.post(url, json=credentials)
        return response

    @staticmethod
    @allure.step("Обновление данных пользователя")
    def update_user(token, update_data):
        url = f"{BASE_URL}{ENDPOINTS['update_user']}"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.patch(url, json=update_data, headers=headers)
        return response

    @staticmethod
    @allure.step("Обновление данных пользователя без авторизации")
    def update_user_without_auth(update_data):
        url = f"{BASE_URL}{ENDPOINTS['update_user']}"
        response = requests.patch(url, json=update_data)
        return response

    @staticmethod
    @allure.step("Удаление пользователя")
    def delete_user(token):
        url = f"{BASE_URL}{ENDPOINTS['delete_user']}"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(url, headers=headers)
        return response


class OrderHelper:

    @staticmethod
    @allure.step("Создание заказа")
    def create_order(token, ingredients):
        url = f"{BASE_URL}{ENDPOINTS['create_order']}"
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        response = requests.post(url, json=ingredients, headers=headers)
        return response

    @staticmethod
    @allure.step("Получение заказов пользователя")
    def get_user_orders(token):
        url = f"{BASE_URL}{ENDPOINTS['get_user_orders']}"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)
        return response

    @staticmethod
    @allure.step("Получение заказов пользователя без авторизации")
    def get_user_orders_without_auth():
        url = f"{BASE_URL}{ENDPOINTS['get_user_orders']}"
        response = requests.get(url)
        return response

    @staticmethod
    @allure.step("Получение списка ингредиентов")
    def get_ingredients():
        url = f"{BASE_URL}{ENDPOINTS['get_ingredients']}"
        response = requests.get(url)
        return response


@allure.step("Извлечение токена из ответа")
def extract_token(response):
    if response.status_code == 200:
        return response.json().get('accessToken')
    return None