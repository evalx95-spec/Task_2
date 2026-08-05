import pytest
import allure
from ..data import TestData
from ..helpers import OrderHelper, UserHelper


@pytest.fixture
def create_and_delete_user():
    max_attempts = 5
    
    for attempt in range(max_attempts):
        user_data = TestData.generate_user_data()
        response = UserHelper.create_user(user_data)
        
        if response.status_code == 200:
            response_data = response.json()
            token = response_data.get('accessToken')
            if token and token.startswith('Bearer '):
                token = token[7:]
            
            yield user_data, token
            
            with allure.step("Удаление созданного пользователя"):
                if token:
                    try:
                        UserHelper.delete_user(token)
                    except Exception as e:
                        allure.attach(str(e), name="Ошибка удаления пользователя", attachment_type=allure.attachment_type.TEXT)
            return
        
        elif response.status_code == 403 and "User already exists" in response.text:
            if attempt == max_attempts - 1:
                pytest.fail(f"Не удалось создать уникального пользователя после {max_attempts} попыток")
            continue
        else:
            pytest.fail(f"Не удалось создать пользователя: {response.status_code}, {response.text}")


@pytest.fixture
def valid_ingredients():
    return TestData.get_valid_ingredients()


@pytest.fixture
def invalid_ingredients():
    return TestData.get_invalid_ingredients()


@pytest.fixture
def empty_ingredients():
    return TestData.get_empty_ingredients()


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
            
            
            assert "Internal Server Error" in response.text or "Error" in response.text, \
                "В ответе должно быть сообщение об ошибке"
            
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
            assert response_data.get('message') == TestData.ERROR_MESSAGES['no_ingredients'], \
                f"Неверное сообщение об ошибке. Ожидалось: {TestData.ERROR_MESSAGES['no_ingredients']}, Получено: {response_data.get('message')}"

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
                allure.attach(
                    "API позволяет создавать заказы без авторизации", 
                    name="Примечание", 
                    attachment_type=allure.attachment_type.TEXT
                )
            else:
                assert response.status_code == 401, f"Ожидался 200 или 401, получен {response.status_code}"
                response_data = response.json()
                assert response_data.get('success') is False, "success должно быть False"