import pytest
import allure
import logging
from helpers import UserHelper, generate_user_data
from data import TestData
from urls import BASE_URL, ENDPOINTS

logger = logging.getLogger(__name__)


@pytest.fixture
def create_and_delete_user():
    """Фикстура для создания уникального пользователя с автоматическим удалением"""
    max_attempts = 5
    
    for attempt in range(max_attempts):
        user_data = generate_user_data()
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
def existing_user():
    """Фикстура для получения существующего пользователя"""
    user_data = TestData.EXISTING_USER.copy()
    token = None
    
    response = UserHelper.create_user(user_data)
    
    if response.status_code == 200:
        token = response.json().get('accessToken')
        if token and token.startswith('Bearer '):
            token = token[7:]
    elif response.status_code == 403 and "User already exists" in response.text:
        login_response = UserHelper.login_user(user_data)
        assert login_response.status_code == 200, "Не удалось залогиниться"
        token = login_response.json().get('accessToken')
        if token and token.startswith('Bearer '):
            token = token[7:]
    else:
        pytest.fail(f"Не удалось создать или получить пользователя: {response.text}")
    
    yield user_data, token
    
    with allure.step("Удаление существующего пользователя"):
        if token:
            try:
                UserHelper.delete_user(token)
            except Exception as e:
                allure.attach(str(e), name="Ошибка удаления", attachment_type=allure.attachment_type.TEXT)


@pytest.fixture
def valid_ingredients():
    """Фикстура для получения валидных ингредиентов"""
    return TestData.get_valid_ingredients()


@pytest.fixture
def invalid_ingredients():
    """Фикстура для получения невалидных ингредиентов"""
    return TestData.get_invalid_ingredients()


@pytest.fixture
def empty_ingredients():
    """Фикстура для получения пустого списка ингредиентов"""
    return TestData.get_empty_ingredients()