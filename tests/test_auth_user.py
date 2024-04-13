import requests
import allure
from data import Urls, ErrorMessage
from helpers import generate_user_data


class TestAuthUser:

    @allure.title('Проверка авторизации пользователя')
    @allure.description('Создаем пользователя, входим по e-mail/password, \
           проверяем, что код ответа: 200, и текст в тексте ответа "success: true"')
    def test_login_user_success(self):
        payload = generate_user_data()
        requests.post(f'{Urls.main_url}{Urls.api_create_user}', data=payload)
        del payload['name']
        response = requests.post(f'{Urls.main_url}{Urls.api_login_user}', data=payload)
        assert response.status_code == 200 and response.json()['success'] == True

    @allure.title('Проверка авторизации с неверным паролем')
    @allure.description('Создаем пользователя, авторизуемся с неверным паролем, \
               проверяем, что код ответа: 401, и текст ответа "email or password are incorrect"')
    def test_login_user_unvalid_password_faild(self):
        payload = generate_user_data()
        requests.post(f'{Urls.main_url}{Urls.api_create_user}', data=payload)
        del payload['name']
        payload['password'] = '123456'
        response = requests.post(f'{Urls.main_url}{Urls.api_login_user}', data=payload)
        assert response.status_code == 401 and response.json()['message'] == ErrorMessage.text_login_401
