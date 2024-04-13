import requests
import allure
from data import Urls, ErrorMessage
from helpers import generate_user_data


class TestUser:

    @allure.title('Проверка успешной регистрации пользователя')
    @allure.description('Создаем пользователя с cгенерированными данными, проверяем, что код ответа: 200,\
                        и в текст ответа содержится accessToken')
    def test_create_user_success(self):
        payload = generate_user_data()
        response = requests.post(f'{Urls.main_url}{Urls.api_create_user}', data=payload)
        token = response.json()['accessToken']
        requests.delete(f'{Urls.main_url}{Urls.api_delete_user}', headers={'Authorization': token})
        assert response.status_code == 200 and 'accessToken' in response.text, (f'Ожидалось 200, получили {response.status_code}, \
                                                                                 ожидалось "acessToken", получили {response.text}')

    @allure.title('Проверка повторной регистрации с повторяющимися данными')
    @allure.description('Создаем пользователя с cгенерированными данными, создаем пользователя с теми же данными, \
    проверяем, что код ответа: 403, и текст ответа "User already exists"')
    def test_create_two_same_user_field(self):
        payload = generate_user_data()
        requests.post(f'{Urls.main_url}{Urls.api_create_user}', data=payload)
        response = requests.post(f'{Urls.main_url}{Urls.api_create_user}', data=payload)
        assert 403 == response.status_code and  response.json()['message'] == ErrorMessage.text_create_403_double

    @allure.title('Проверка регистрации без e-mail')
    @allure.description('Создаем пользователя без указания e-mail, \
        проверяем, что код ответа: 403, и текст ответа "Email, password and name are required fields"')
    def test_create_user_without_email_field(self):
        payload = generate_user_data()
        del payload['email']
        response = requests.post(f'{Urls.main_url}{Urls.api_create_user}', data=payload)
        assert 403 == response.status_code and response.json()['message'] == ErrorMessage.text_create_403_wrong


