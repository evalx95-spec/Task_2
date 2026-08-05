import pytest
import allure
from ..data import TestData
from ..helpers import OrderHelper


class TestGetOrderUser:

    @allure.title("Получение заказов авторизованного пользователя")
    @allure.description("Проверка успешного получения списка заказов авторизованным пользователем")
    def test_get_order_user_with_auth(self, create_and_delete_user, valid_ingredients):
        
        user_data, token = create_and_delete_user
        
        with allure.step("Создание заказа для пользователя"):
            ingredients = valid_ingredients
            create_response = OrderHelper.create_order(token, ingredients)
            assert create_response.status_code == 200, "Не удалось создать заказ"
            allure.attach(f"Создан заказ с ингредиентами: {ingredients['ingredients']}", 
                         name="Создание заказа", 
                         attachment_type=allure.attachment_type.TEXT)
        
        with allure.step("Получение заказов пользователя"):
            response = OrderHelper.get_user_orders(token)
        
        with allure.step("Проверка успешного получения заказов"):
            assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
            response_data = response.json()
            
            
            assert response_data.get('success') is True, "success должно быть True"
            assert 'orders' in response_data, "В ответе должен быть список orders"
            assert response_data['orders'] is not None, "Список заказов не должен быть пустым"
            
            
            assert len(response_data['orders']) > 0, "Должен быть хотя бы один заказ"
            
            
            order = response_data['orders'][0]
            assert 'number' in order, "В заказе должен быть номер"
            assert 'ingredients' in order, "В заказе должны быть ингредиенты"
            assert 'status' in order, "В заказе должен быть статус"
            
            allure.attach(f"Найден заказ №{order.get('number')} со статусом {order.get('status')}", 
                         name="Результат", 
                         attachment_type=allure.attachment_type.TEXT)

    @allure.title("Получение заказов без авторизации")
    @allure.description("Проверка ошибки при получении заказов без токена авторизации")
    def test_get_order_user_without_auth(self):

        with allure.step("Попытка получения заказов без токена"):
            response = OrderHelper.get_user_orders_without_auth()
        
        with allure.step("Проверка ответа с ошибкой"):
            assert response.status_code == 401, f"Ожидался 401, получен {response.status_code}"
            response_data = response.json()
            
            assert response_data.get('success') is False, "success должно быть False"
            assert response_data.get('message') == TestData.ERROR_MESSAGES['unauthorized'], \
                f"Неверное сообщение об ошибке. Ожидалось: {TestData.ERROR_MESSAGES['unauthorized']}, Получено: {response_data.get('message')}"
            
            allure.attach(f"Ошибка: {response_data.get('message')}", 
                         name="Результат", 
                         attachment_type=allure.attachment_type.TEXT)
    
    @allure.title("Получение заказов с неверным токеном")
    @allure.description("Проверка ошибки при получении заказов с неверным токеном авторизации")
    def test_get_order_user_invalid_token(self):
        
        invalid_token = "invalid_token_12345"
        
        with allure.step("Попытка получения заказов с неверным токеном"):
            response = OrderHelper.get_user_orders(invalid_token)
        
        with allure.step("Проверка ответа с ошибкой"):
            
            assert response.status_code in [401, 403], f"Ожидался 401 или 403, получен {response.status_code}"
            
           
            response_data = response.json()
            assert response_data.get('success') is False, "success должно быть False"
            
            allure.attach(f"Статус: {response.status_code}, Сообщение: {response_data.get('message')}", 
                         name="Результат", 
                         attachment_type=allure.attachment_type.TEXT)
    
    @allure.title("Получение заказов без созданных заказов")
    @allure.description("Проверка получения пустого списка заказов у нового пользователя")
    def test_get_order_user_empty_orders(self, create_and_delete_user):
        
        user_data, token = create_and_delete_user
        
        with allure.step("Получение заказов пользователя без создания заказов"):
            response = OrderHelper.get_user_orders(token)
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
            response_data = response.json()
            
            assert response_data.get('success') is True, "success должно быть True"
            assert 'orders' in response_data, "В ответе должен быть список orders"
            assert response_data['orders'] is not None, "Список заказов не должен быть None"
            assert len(response_data['orders']) == 0, f"Ожидался пустой список, получено {len(response_data['orders'])} заказов"
            
            allure.attach("У пользователя нет заказов (ожидаемое поведение)", 
                         name="Результат", 
                         attachment_type=allure.attachment_type.TEXT)