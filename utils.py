import allure


@allure.step("Извлечение токена из ответа")
def extract_token(response):
    """Извлекает и очищает токен из ответа API"""
    if response.status_code == 200:
        token = response.json().get('accessToken')
        if token and token.startswith('Bearer '):
            return token[7:]
        return token
    return None
