from faker import Faker

fake = Faker()

class TestData:

    @staticmethod
    def generate_user_data():
        """Генерация случайных данных пользователя"""
        return {
            "email": fake.email(),
            "password": fake.password(length=8),
            "name": fake.first_name()
        }

    @staticmethod
    def generate_user_without_field(field_to_remove):
        """Генерация данных пользователя без указанного поля"""
        user_data = TestData.generate_user_data()
        if field_to_remove in user_data:
            del user_data[field_to_remove]
        return user_data

    EXISTING_USER = {
        "email": "evalx95@gmail.com",
        "password": "tests123",
        "name": "Jenya"
    }

    INVALID_CREDENTIALS = {
        "email": "test111@mail.ru",
        "password": "testtest"
    }

    INVALID_LOGIN_CASES = [
        {
            "email": "wrong@example.com",
            "password": "test111"
        },
        {
            "email": "testsuser@example.com",
            "password": "wrongtest"
        },
        {
            "email": "wrong@example.com",
            "password": "wrongpassword"
        }
    ]

    
    DEFAULT_INGREDIENTS = ["60d3b41abdacab0026a733c6", "61c0c5a71d1f82001bdaaa6f"]
    
    @staticmethod
    def get_valid_ingredients():
        """Возвращает валидные ингредиенты для создания заказа"""
        return {
            "ingredients": TestData.DEFAULT_INGREDIENTS
        }
    
    @staticmethod
    def get_invalid_ingredients():
        """Возвращает невалидные ингредиенты для тестов ошибок"""
        return {
            "ingredients": ["invalid_hash_1", "invalid_hash_2"]
        }
    
    @staticmethod
    def get_empty_ingredients():
        """Возвращает пустой список ингредиентов"""
        return {
            "ingredients": []
        }
    
    @staticmethod
    def get_single_ingredient():
        """Возвращает один ингредиент"""
        return {
            "ingredients": [TestData.DEFAULT_INGREDIENTS[0]]
        }

    ERROR_MESSAGES = {
        "user_exists": "User already exists",
        "missing_fields": "Email, password and name are required fields",
        "invalid_credentials": "email or password are incorrect",
        "unauthorized": "You should be authorised",
        "invalid_ingredient": "Internal Server Error",
        "no_ingredients": "Ingredient ids must be provided"
    }