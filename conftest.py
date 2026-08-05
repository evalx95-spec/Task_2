import pytest
import requests
import logging
import allure
from .data import TestData
from .helpers import UserHelper
from .urls import BASE_URL, ENDPOINTS

logger = logging.getLogger(__name__)


@pytest.fixture
def create_unique_user():
    
    max_attempts = 5
    token = None

    for attempt in range(max_attempts):
        user_data = TestData.generate_user_data()
        response = UserHelper.create_user(user_data)

        if response.status_code == 200:
            token = response.json().get('accessToken')
            if not token:
                pytest.fail("No accessToken in response")

            if token.startswith('Bearer '):
                token = token[7:]

            yield user_data, token

            try:
                UserHelper.delete_user(token)
            except Exception as e:
                logger.warning(f"Could not delete user: {e}")
            return
            
        elif response.status_code == 403 and "User already exists" in response.text:
            if attempt == max_attempts - 1:
                pytest.fail(f"Failed to create unique user after {max_attempts} attempts. Last error: {response.text}")
            continue
        else:
            pytest.fail(f"Failed to create user: {response.status_code}, {response.text}")


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
                        logger.info(f"User {user_data['email']} successfully deleted")
                    except Exception as e:
                        logger.warning(f"Could not delete user {user_data['email']}: {e}")
                        allure.attach(str(e), name="Ошибка удаления пользователя", attachment_type=allure.attachment_type.TEXT)
            return
        
        elif response.status_code == 403 and "User already exists" in response.text:
            if attempt == max_attempts - 1:
                pytest.fail(f"Failed to create unique user after {max_attempts} attempts. Last error: {response.text}")
            continue
        else:
            pytest.fail(f"Failed to create user: {response.status_code}, {response.text}")


@pytest.fixture
def existing_user():
    
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
def auth_token(existing_user):
    
    _, token = existing_user
    return token


@pytest.fixture
def valid_ingredients():
    
    response = requests.get(f"{BASE_URL}{ENDPOINTS['get_ingredients']}")
    
    if response.status_code == 200:
        ingredients = response.json().get('data', [])
        if len(ingredients) >= 2:
            return {
                "ingredients": [ingredients[0]['_id'], ingredients[1]['_id']]
            }
    
    
    return {
        "ingredients": TestData.DEFAULT_INGREDIENTS
    }


@pytest.fixture
def invalid_ingredients():
    
    return TestData.get_invalid_ingredients()


@pytest.fixture
def empty_ingredients():
    
    return TestData.get_empty_ingredients()


@pytest.fixture(autouse=True)
def cleanup_existing_users():
    
    try:
        login_response = UserHelper.login_user(TestData.EXISTING_USER)
        if login_response.status_code == 200:
            token = login_response.json().get('accessToken')
            if token and token.startswith('Bearer '):
                token = token[7:]
            UserHelper.delete_user(token)
            logger.info("Existing user cleaned up")
    except Exception as e:
        logger.warning(f"Could not cleanup existing user: {e}")