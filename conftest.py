import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest
import allure
import logging
from helpers import generate_user_data
from api_client import UserAPI, OrderAPI
from utils import extract_token
from data import TestData
from urls import BASE_URL, ENDPOINTS

logger = logging.getLogger(__name__)


@pytest.fixture
def create_and_delete_user():
    """Фикстура для создания уникального пользователя с автоматическим удалением"""
    max_attempts = 5
    
    for attempt in range(max_attempts):
        user_data = generate_user_data()
        response = UserAPI.create_user(user_data)
        
        if response.status_code == 200:
            response_data = response.json()
            token = extract_token(response)
            
            yield user_data, response_data, token
            
            with allure.step("Удаление созданного пользователя"):
                if token:
                    try:
                        UserAPI.delete_user(token)
                    except Exception as e:
                        allure.attach(
                            str(e), 
                            name="Ошибка удаления пользователя", 
                            attachment_type=allure.attachment_type.TEXT
                        )
            return
        
        elif response.status_code == 403 and "User already exists" in response.text:
            if attempt == max_attempts - 1:
                pytest.fail(
                    f"Не удалось создать уникального пользователя после {max_attempts} попыток"
                )
            continue
        else:
            pytest.fail(
                f"Не удалось создать пользователя: {response.status_code}, {response.text}"
            )


@pytest.fixture
def existing_user():
    """Фикстура для получения существующего пользователя"""
    user_data = TestData.EXISTING_USER.copy()
    token = None
    
    response = UserAPI.create_user(user_data)
    
    if response.status_code == 200:
        token = extract_token(response)
    elif response.status_code == 403 and "User already exists" in response.text:
        login_response = UserAPI.login_user(user_data)
        if login_response.status_code != 200:
            pytest.fail(
                f"Не удалось залогиниться: {login_response.status_code}, {login_response.text}"
            )
        token = extract_token(login_response)
    else:
        pytest.fail(f"Не удалось создать или получить пользователя: {response.text}")
    
    yield user_data, token
    
    with allure.step("Удаление существующего пользователя"):
        if token:
            try:
                UserAPI.delete_user(token)
            except Exception as e:
                allure.attach(
                    str(e), 
                    name="Ошибка удаления", 
                    attachment_type=allure.attachment_type.TEXT
                )