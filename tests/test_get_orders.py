import requests
import allure
from data import Urls, ErrorMessage


class TestGetOrders:
    @allure.title('Проверка получения заказов пользователя без авторизации')
    @allure.description('Отправляем запрос на получение закаков без передачи токена, проверяем что код ответа 401 и текст\
                        ответа "You should be authorised"')
    def test_get_order_without_auth_faild(self):
        response = requests.get(f'{Urls.main_url}{Urls.api_create_order}')
        assert response.status_code == 401 and response.json()['message'] == ErrorMessage.text_get_orders_no_auth

    @allure.title('Проверка получения заказов авторизованного пользователя')
    @allure.description('Создаем пользователя, создаем заказ, Отправляем запрос на получение закаков с токеном авторизации, \
     проверяем что код ответа 200 и в текстe ответа "orders"')
    def test_order_auth_success(self, create_user_and_get_token, get_ingredient_hash):
        token = create_user_and_get_token
        ingredients = {'ingredients': [get_ingredient_hash['data'][0]['_id'], get_ingredient_hash['data'][2]['_id'], get_ingredient_hash['data'][7]['_id']]}
        requests.post(f'{Urls.main_url}{Urls.api_create_order}', data=ingredients)
        response = requests.get(f'{Urls.main_url}{Urls.api_create_order}', headers={'Authorization':token})
        assert response.status_code == 200 and "orders" in response.text
