import requests
import allure
from data import Data

class TestOrder:

    @allure.title('Проверка создания заказа с авторизацией')
    @allure.description('Создаем пользователя, автриизуемся, создаем заказ, проверяем, что в ответе "success: True",\
                        и name заказа соответствует заказанным ингредиентам')
    def test_create_order_auth_success(self, create_user_and_get_token, get_ingredient_hash):
        requests.post(f'{Data.main_url}{Data.api_login_user}', data=create_user_and_get_token)
        ingredients = {'ingredients': [get_ingredient_hash['data'][0]['_id'], get_ingredient_hash['data'][2]['_id'], get_ingredient_hash['data'][7]['_id']]}
        response = requests.post(f'{Data.main_url}{Data.api_create_order}', data=ingredients)
        order = response.json()
        assert order['name'] == 'Метеоритный флюоресцентный традиционный-галактический бургер' and order['success'] == True

    @allure.title('Проверка создания заказа без авторизации')
    @allure.description('Создаем заказ, проверяем, что в ответе "success: True",\
                            и name заказа соответствует заказанным ингредиентам')
    def test_create_order_no_auth_success(self, get_ingredient_hash):
        ingredients = {'ingredients': [get_ingredient_hash['data'][1]['_id'], get_ingredient_hash['data'][3]['_id'], get_ingredient_hash['data'][6]['_id']]}
        response = requests.post(f'{Data.main_url}{Data.api_create_order}', data=ingredients)
        order = response.json()
        assert order['name'] == 'Space бессмертный био-марсианский бургер' and order['success'] == True

    @allure.title('Проверка создания заказа без ингредиентов')
    @allure.description('Создаем заказ не передавая ингредиенты, проверяем, что код ответа 400,\
                                и текст ответа "Ingredient ids must be provided"')
    def test_create_order_without_ingredients_faild(self, get_ingredient_hash):
        ingredients = {'ingredients': []}
        response = requests.post(f'{Data.main_url}{Data.api_create_order}', data=ingredients)
        assert response.status_code == 400 and response.json()['message'] == Data.text_order_without_ingredients

    @allure.title('Проверка создания заказа c ингредиентами')
    @allure.description('Создаем заказ передавая ингредиенты, проверяем, что в ответе "success: True",\
                            и name заказа соответствует заказанным ингредиентам')
    def test_create_order_with_ingredients_success(self, create_user_and_get_token, get_ingredient_hash):
        ingredients = {'ingredients': [get_ingredient_hash['data'][1]['_id'], get_ingredient_hash['data'][4]['_id'], get_ingredient_hash['data'][8]['_id']]}
        response = requests.post(f'{Data.main_url}{Data.api_create_order}', data=ingredients)
        order = response.json()
        assert order['name'] == 'Spicy бессмертный краторный бургер' and order['success'] == True

    @allure.title('Проверка создания заказа c неверными хэш ингредиентов')
    @allure.description('Создаем заказ передавая неверный хэш ингредиента, проверяем, что код ответа 500')
    def test_create_order_with_unvalid_hash_ingredients_faild(self, get_ingredient_hash):
        ingredients = {'ingredients': [Data.f_hash, Data.f_hash]}
        response = requests.post(f'{Data.main_url}{Data.api_create_order}', data=ingredients)
        assert response.status_code == 500

    @allure.title('Проверка получения заказов пользователя без авторизации')
    @allure.description('Отправляем запрос на получение закаков без передачи токена, проверяем что код ответа 401 и текст\
                        ответа "You should be authorised"')
    def test_get_order_without_auth_faild(self):
        response = requests.get(f'{Data.main_url}{Data.api_create_order}')
        assert response.status_code == 401 and response.json()['message'] == Data.text_get_orders_no_auth

    @allure.title('Проверка получения заказов авторизованного пользователя')
    @allure.description('Создаем пользователя, создаем заказ, Отправляем запрос на получение закаков с токеном авторизации, \
     проверяем что код ответа 200 и в текстe ответа "orders"')
    def test_order_auth_success(self, create_user_and_get_token, get_ingredient_hash):
        token = create_user_and_get_token
        ingredients = {'ingredients': [get_ingredient_hash['data'][0]['_id'], get_ingredient_hash['data'][2]['_id'], get_ingredient_hash['data'][7]['_id']]}
        requests.post(f'{Data.main_url}{Data.api_create_order}', data=ingredients)
        response = requests.get(f'{Data.main_url}{Data.api_create_order}', headers={'Authorization':token})
        assert response.status_code == 200 and "orders" in response.text







