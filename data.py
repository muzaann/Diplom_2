from faker import Faker
from random import randint


class Data:
    Faker.seed(randint(1000, 10000))
    faker = Faker()

    login = faker.user_name()
    password = faker.password()
    email = faker.email()
    f_hash = faker.md5(raw_output=False)

    main_url = "https://stellarburgers.nomoreparties.site"
    api_create_user = "/api/auth/register"
    api_login_user = "/api/auth/login"
    api_order = "/api/v1/orders"
    api_delete_user = "/api/auth/user"
    api_get_user = '/api/auth/user'
    api_get_ingredients = "/api/ingredients"
    api_create_order = "/api/orders"

    text_login_401 = 'email or password are incorrect'
    text_login_404 = "Учетная запись не найдена"
    text_create_403_double = "User already exists"
    text_create_403_wrong = "Email, password and name are required fields"
    text_create_400 = "Недостаточно данных для создания учетной записи"
    text_update_401 = "You should be authorised"
    text_order_without_ingredients = "Ingredient ids must be provided"
    text_get_orders_no_auth = "You should be authorised"
