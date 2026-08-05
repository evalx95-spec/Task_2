import pytest
import allure
from ..data import TestData
from ..helpers import UserHelper


@pytest.fixture
def create_and_delete_user():
    user_data = TestData.generate_user_data()
    response = UserHelper.create_user(user_data)
    assert response.status_code == 200, f"Не удалось создать пользователя: {response.text}"
    
    response_data = response.json()
    token = response_data.get('accessToken')
    if token and token.startswith('Bearer '):
        token = token[7:]
    
    allure.attach(f"Создан пользователь: {user_data['email']}", name="Создание пользователя", attachment_type=allure.attachment_type.TEXT)
    
    yield user_data, response_data, token
    
    with allure.step("Удаление созданного пользователя"):
        if token:
            try:
                delete_response = UserHelper.delete_user(token)
                if delete_response.status_code == 202:
                    allure.attach("Пользователь успешно удален", name="Результат очистки", attachment_type=allure.attachment_type.TEXT)
                else:
                    allure.attach(f"Неожиданный статус удаления: {delete_response.status_code}", name="Результат очистки", attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                allure.attach(str(e), name="Ошибка удаления пользователя", attachment_type=allure.attachment_type.TEXT)
                pytest.fail(f"Не удалось удалить пользователя: {e}")


@pytest.fixture
def existing_user():
    user_data = TestData.EXISTING_USER.copy()
    token = None
    
    response = UserHelper.create_user(user_data)
    
    if response.status_code == 200:
        token = response.json().get('accessToken')
        if token and token.startswith('Bearer '):
            token = token[7:]
        allure.attach("Создан новый пользователь", name="Подготовка", attachment_type=allure.attachment_type.TEXT)
    elif response.status_code == 403 and "User already exists" in response.text:
        
        login_response = UserHelper.login_user(user_data)
        assert login_response.status_code == 200, "Не удалось залогиниться"
        token = login_response.json().get('accessToken')
        if token and token.startswith('Bearer '):
            token = token[7:]
        allure.attach("Использован существующий пользователь", name="Подготовка", attachment_type=allure.attachment_type.TEXT)
    else:
        pytest.fail(f"Не удалось создать или получить пользователя: {response.text}")
    
    yield user_data, token
    
    with allure.step("Удаление существующего пользователя"):
        if token:
            try:
                UserHelper.delete_user(token)
                allure.attach("Пользователь удален", name="Результат очистки", attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                allure.attach(str(e), name="Ошибка удаления", attachment_type=allure.attachment_type.TEXT)


class TestUserCreation:

    @allure.title("Создание уникального пользователя")
    @allure.description("Проверка успешного создания нового уникального пользователя")
    def test_create_unique_user(self, create_and_delete_user):
        user_data, response_data, token = create_and_delete_user
        
        with allure.step("Проверка данных созданного пользователя"):
            assert response_data.get('success') is True, "success должно быть True"
            
            user = response_data.get('user', {})
            assert user.get('email') == user_data['email'], "Email не совпадает"
            assert user.get('name') == user_data['name'], "Name не совпадает"
            
            assert 'accessToken' in response_data, "Отсутствует accessToken"
            assert 'refreshToken' in response_data, "Отсутствует refreshToken"
            
            allure.attach(f"Пользователь {user_data['email']} успешно создан", name="Результат теста", attachment_type=allure.attachment_type.TEXT)

    @allure.title("Создание существующего пользователя")
    @allure.description("Проверка ошибки при попытке создать уже зарегистрированного пользователя")
    def test_create_existing_user(self, existing_user):
        user_data, _ = existing_user
        
        with allure.step("Попытка создать дубликат пользователя"):
            response = UserHelper.create_user(user_data)
        
        with allure.step("Проверка ответа с ошибкой"):
            assert response.status_code == 403, "Ожидался статус 403"
            
            response_data = response.json()
            assert response_data.get('success') is False, "success должно быть False"
            assert response_data.get('message') == TestData.ERROR_MESSAGES['user_exists'], "Неверное сообщение об ошибке"
            
            allure.attach(f"Попытка создать дубликат {user_data['email']} вернула ошибку", name="Результат теста", attachment_type=allure.attachment_type.TEXT)

    @allure.title("Создание пользователя без обязательного поля")
    @allure.description("Проверка ошибки при попытке создать пользователя без одного из обязательных полей")
    @pytest.mark.parametrize("field_to_remove", ['email', 'password', 'name'])
    def test_create_user_without_field(self, field_to_remove):
        with allure.step(f"Генерация данных без поля '{field_to_remove}'"):
            user_data = TestData.generate_user_without_field(field_to_remove)
            allure.attach(f"Отсутствует поле: {field_to_remove}", name="Параметры теста", attachment_type=allure.attachment_type.TEXT)
        
        with allure.step("Отправка запроса на создание пользователя"):
            response = UserHelper.create_user(user_data)
        
        with allure.step("Проверка ответа с ошибкой"):
            assert response.status_code == 403, "Ожидался статус 403"
            
            response_data = response.json()
            assert response_data.get('success') is False, "success должно быть False"
            assert response_data.get('message') == TestData.ERROR_MESSAGES['missing_fields'], "Неверное сообщение об ошибке"
            
            assert 'accessToken' not in response_data, "Пользователь не должен создаваться без обязательных полей"
            
            allure.attach(f"Запрос без поля {field_to_remove} вернул ошибку", name="Результат теста", attachment_type=allure.attachment_type.TEXT)