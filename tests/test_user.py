import pytest
import requests
import allure
from data import Data


class TestUser:

    @allure.title('Проверка успешной регистрации пользователя')
    @allure.description('Создаем пользователя с cгенерированными данными, проверяем, что код ответа: 200,\
                        и в текст ответа содержится accessToken')
    def test_create_user_success(self, generate_user_data):
        response = requests.post(f'{Data.main_url}{Data.api_create_user}', data=generate_user_data)
        token = response.json()['accessToken']
        requests.delete(f'{Data.main_url}{Data.api_delete_user}', headers={'Authorization': token})
        assert response.status_code == 200 and 'accessToken' in response.text, (f'Ожидалось 200, получили {response.status_code}, \
                                                                                 ожидалось "acessToken", получили {response.text}')

    @allure.title('Проверка повторной регистрации с повторяющимися данными')
    @allure.description('Создаем пользователя с cгенерированными данными, создаем пользователя с теми же данными, \
    проверяем, что код ответа: 403, и текст ответа "User already exists"')
    def test_create_two_same_user_field(self, generate_user_data):
        requests.post(f'{Data.main_url}{Data.api_create_user}', data=generate_user_data)
        response = requests.post(f'{Data.main_url}{Data.api_create_user}', data=generate_user_data)
        assert 403 == response.status_code and  response.json()['message'] == Data.text_create_403_double

    @allure.title('Проверка регистрации без e-mail')
    @allure.description('Создаем пользователя без указания e-mail, \
        проверяем, что код ответа: 403, и текст ответа "Email, password and name are required fields"')
    def test_create_user_without_email_field(self, generate_user_data):
        del generate_user_data['email']
        response = requests.post(f'{Data.main_url}{Data.api_create_user}', data=generate_user_data)
        assert 403 == response.status_code and response.json()['message'] == Data.text_create_403_wrong

    @allure.title('Проверка авторизации пользователя')
    @allure.description('Создаем пользователя, входим по e-mail/password, \
        проверяем, что код ответа: 200, и текст в тексте ответа "success: true"')
    def test_login_user_success(self, generate_user_data):
        requests.post(f'{Data.main_url}{Data.api_create_user}', data=generate_user_data)
        del generate_user_data['name']
        response = requests.post(f'{Data.main_url}{Data.api_login_user}', data=generate_user_data)
        assert response.status_code == 200 and response.json()['success'] == True


    @allure.title('Проверка авторизации с неверным паролем')
    @allure.description('Создаем пользователя, авторизуемся с неверным паролем, \
            проверяем, что код ответа: 401, и текст ответа "email or password are incorrect"')
    def test_login_user_unvalid_password_faild(self, generate_user_data):
        requests.post(f'{Data.main_url}{Data.api_create_user}', data=generate_user_data)
        del generate_user_data['name']
        generate_user_data['password'] = '123456'
        response = requests.post(f'{Data.main_url}{Data.api_login_user}', data=generate_user_data)
        assert response.status_code == 401 and  response.json()['message'] == Data.text_login_401


    @allure.title('Параметризованная проверка успешного изменения пользователя при изменении логина/email с авторизацией')
    @allure.description('Создаем пользователя, получаем данные пользователя, меняем имя/email, отправляем \
                           запрос на изменение данных с токеном, проверяем что в ответе приходит статус-код\
                            200 и {"success}: True')
    @pytest.mark.parametrize('update_argument, update_data', (['name', Data.login], ['email', Data.email]))
    def test_update_user_data_success(self, create_user_and_get_token, update_argument, update_data):
        user_data = requests.get(f'{Data.main_url}{Data.api_get_user}', headers={'Authorization': create_user_and_get_token})
        user_data.json()['user'][update_argument] = update_data
        update_user = requests.patch(f'{Data.main_url}{Data.api_get_user}', data=user_data,
                                     headers={'Authorization': create_user_and_get_token})
        assert update_user.status_code == 200 and update_user.json()['success'] == True

    @allure.title('Проверка невозможности изменения пользователя без авторизации')
    @allure.description('Создаем пользователя, получаем данные пользователя, меняем имя, отправляем \
                       запрос на изменение данных без токена, проверяем что в ответе приходит ошибка\
                        401 и текст "You should be authorised"')
    def test_update_user_data_no_auth_faild(self, create_user_and_get_token):
        user_data = requests.get(f'{Data.main_url}{Data.api_get_user}', headers={'Authorization': create_user_and_get_token})
        user_data.json()['user']['name'] = Data.login
        update_user = requests.patch(f'{Data.main_url}{Data.api_get_user}', data=user_data)
        assert update_user.status_code == 401 and update_user.json()['message'] == Data.text_update_401

