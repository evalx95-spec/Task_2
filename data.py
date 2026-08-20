class TestData:

    EXISTING_USER = {
        "email": "evalx95@gmail.com",
        "password": "tests123",
        "name": "Jenya"
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

    ERROR_MESSAGES = {
        "user_exists": "User already exists",
        "missing_fields": "Email, password and name are required fields",
        "invalid_credentials": "email or password are incorrect",
        "unauthorized": "You should be authorised",
        "no_ingredients": "Ingredient ids must be provided"
    }
