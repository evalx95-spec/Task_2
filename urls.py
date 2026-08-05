BASE_URL = "https://stellarburgers.education-services.ru"

ENDPOINTS = {
    "create_user": "/api/auth/register",
    "login_user": "/api/auth/login",
    "update_user": "/api/auth/user",
    "delete_user": "/api/auth/user",
    "logout_user": "/api/auth/logout",
    "create_order": "/api/orders",
    "get_user_orders": "/api/orders",
    "get_ingredients": "/api/ingredients"
}


INGREDIENTS = {
    "valid": {
        "ingredients": ["60d3b41abdacab0026a733c6", "61c0c5a71d1f82001bdaaa6f"]
    },
    "invalid": {
        "ingredients": ["invalid_hash_1", "invalid_hash_2"]
    },
    "empty": {
        "ingredients": []
    },
    "real": [
        "60d3b41abdacab0026a733c6",  
        "609646e4dc916e00276b2870",  
        "61c0c5a71d1f82001bdaaa72",  
        "61c0c5a71d1f82001bdaaa74",  
        "61c0c5a71d1f82001bdaaa76",  
    ],
    
    "single": {
        "ingredients": ["61c0c5a71d1f82001bdaaa6d"]
    },
    
    "many": {
        "ingredients": [
            "60d3b41abdacab0026a733c6",
            "609646e4dc916e00276b2870",
            "61c0c5a71d1f82001bdaaa72",
            "61c0c5a71d1f82001bdaaa74",
            "61c0c5a71d1f82001bdaaa76"
        ]
    }
}


def get_ingredient_ids(count=2):
    """
    Возвращает указанное количество ID ингредиентов из списка real
    """
    return INGREDIENTS["real"][:count]

def get_valid_ingredients():
    """
    Возвращает валидные ингредиенты для создания заказа
    """
    return INGREDIENTS["valid"]

def get_invalid_ingredients():
    """
    Возвращает невалидные ингредиенты для тестов ошибок
    """
    return INGREDIENTS["invalid"]

def get_empty_ingredients():
    """
    Возвращает пустой список ингредиентов
    """
    return INGREDIENTS["empty"]