import pytest
import requests
from data import Data


@pytest.fixture()
def generate_user_data():
    payload = {
        "email": Data.email,
        "password": Data.password,
        "name": Data.login
    }
    return payload

@pytest.fixture()
def create_user_and_get_token(generate_user_data):
    requests.post(f'{Data.main_url}{Data.api_create_user}', data=generate_user_data)
    del generate_user_data['name']
    response = requests.post(f'{Data.main_url}{Data.api_login_user}', data=generate_user_data)
    token = response.json()['accessToken']
    yield token
    requests.delete(f'{Data.main_url}{Data.api_delete_user}', headers={'Authorization':token})

@pytest.fixture()
def create_and_login_user(generate_user_data):
    requests.post(f'{Data.main_url}{Data.api_create_user}', data=generate_user_data)
    del generate_user_data['name']
    response = requests.post(f'{Data.main_url}{Data.api_login_user}', data=generate_user_data)
    yield response

@pytest.fixture()
def get_ingredient_hash():
    response = requests.get(f'{Data.main_url}{Data.api_get_ingredients}')
    ingredients = response.json()
    yield ingredients
