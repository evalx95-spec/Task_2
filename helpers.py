import requests
import allure
from urls import BASE_URL, ENDPOINTS


class UserHelper:

    @staticmethod
    @allure.step("Создание нового пользователя")  # Убираем подстановку параметров
    def create_user(user_data):
        url = f"{BASE_URL}{ENDPOINTS['create_user']}"
        response = requests.post(url, json=user_data)
        
        # Добавляем информацию в отчет отдельно
        if isinstance(user_data, dict) and 'email' in user_data:
            allure.attach(f"Email: {user_data['email']}", name="Данные пользователя", attachment_type=allure.attachment_type.TEXT)
        
        return response

    @staticmethod
    @allure.step("Авторизация пользователя")  # Убираем подстановку параметров
    def login_user(credentials):
        url = f"{BASE_URL}{ENDPOINTS['login_user']}"
        response = requests.post(url, json=credentials)
        
        if isinstance(credentials, dict) and 'email' in credentials:
            allure.attach(f"Email: {credentials['email']}", name="Учетные данные", attachment_type=allure.attachment_type.TEXT)
        
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
        
        if isinstance(ingredients, dict) and 'ingredients' in ingredients:
            allure.attach(f"Количество ингредиентов: {len(ingredients['ingredients'])}", 
                         name="Данные заказа", 
                         attachment_type=allure.attachment_type.TEXT)
        
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