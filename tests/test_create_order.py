import pytest
import allure
from helpers import UserHelper, OrderHelper
from data import TestData


class TestCreateOrder:

    @allure.title("Создание заказа авторизованным пользователем")
    @allure.description("Проверка успешного создания заказа с ингредиентами")
    def test_create_order_success(self, create_and_delete_user, valid_ingredients):
        _, token = create_and_delete_user
        ingredients = valid_ingredients
        
        with allure.step("Создание заказа"):
            response = OrderHelper.create_order(token, ingredients)
        
        with allure.step("Проверка успешного создания заказа"):
            assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
            response_data = response.json()
            assert response_data.get('success') is True, "success должно быть True"
            assert 'order' in response_data, "В ответе отсутствует order"
            assert 'number' in response_data['order'], "В заказе отсутствует number"

    @allure.title("Создание заказа с невалидными ингредиентами")
    @allure.description("Проверка ошибки при создании заказа с невалидными хэшами ингредиентов")
    def test_create_order_invalid_ingredients(self, create_and_delete_user, invalid_ingredients):
        _, token = create_and_delete_user
        ingredients = invalid_ingredients
        
        with allure.step("Создание заказа с невалидными ингредиентами"):
            response = OrderHelper.create_order(token, ingredients)
        
        with allure.step("Проверка ответа с ошибкой"):
            assert response.status_code == 500, f"Ожидался 500, получен {response.status_code}"
            assert "Internal Server Error" in response.text, "В ответе должно быть сообщение об ошибке"
            
            allure.attach(
                f"Статус: {response.status_code}\nТело ответа: {response.text[:500]}", 
                name="Детали ошибки", 
                attachment_type=allure.attachment_type.TEXT
            )

    @allure.title("Создание заказа без ингредиентов")
    @allure.description("Проверка ошибки при создании заказа без ингредиентов")
    def test_create_order_empty_ingredients(self, create_and_delete_user, empty_ingredients):
        _, token = create_and_delete_user
        ingredients = empty_ingredients
        
        with allure.step("Создание заказа без ингредиентов"):
            response = OrderHelper.create_order(token, ingredients)
        
        with allure.step("Проверка ответа с ошибкой"):
            assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}"
            response_data = response.json()
            assert response_data.get('success') is False, "success должно быть False"
            assert response_data.get('message') == TestData.ERROR_MESSAGES['no_ingredients'], "Неверное сообщение об ошибке"

    @allure.title("Создание заказа без авторизации")
    @allure.description("Проверка поведения API при создании заказа без токена")
    def test_create_order_without_auth(self, valid_ingredients):
        ingredients = valid_ingredients
        
        with allure.step("Попытка создания заказа без токена"):
            response = OrderHelper.create_order(None, ingredients)
        
        with allure.step("Проверка ответа"):
            if response.status_code == 200:
                response_data = response.json()
                assert response_data.get('success') is True, "Заказ должен создаваться"
                assert 'order' in response_data, "В ответе должен быть order"
                allure.attach("API позволяет создавать заказы без авторизации", 
                            name="Примечание", 
                            attachment_type=allure.attachment_type.TEXT)
            else:
                assert response.status_code == 401, f"Ожидался 200 или 401, получен {response.status_code}"
                response_data = response.json()
                assert response_data.get('success') is False, "success должно быть False"