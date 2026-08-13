import allure
from faker import Faker

fake = Faker()


def generate_user_data():
    """Генерация случайных данных пользователя"""
    return {
        "email": fake.email(),
        "password": fake.password(length=8),
        "name": fake.first_name()
    }


def generate_user_without_field(field_to_remove):
    """Генерация данных пользователя без указанного поля"""
    user_data = generate_user_data()
    if field_to_remove in user_data:
        del user_data[field_to_remove]
    return user_data