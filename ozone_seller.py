import requests


class OzoneSeller:

    def __init__(self, data):
        self.id = data['id']
        self.key = data['key']
        self.url = data['url']
        self.version = data['version']

    def get_headers(self):
        return {
            'Client-id': self.id,
            'Api-Key': self.key,
        }

    '''Получение всех акций'''
    def get_actions(self):
        url = self.url + self.version + "/actions"
        headers = self.get_headers()
        result = requests.get(url, headers=headers)
        all_actions = {}
        if result.status_code == 200:
            all_actions = result.json()['result']
        else:
            print(result.json()['message'])
        return all_actions

    '''Получение товаров подходящих к акции'''
    def get_candidates(self, action_id):
        url = self.url + self.version + "/actions/candidates"
        headers = self.get_headers()
        params = {
            "action_id": action_id,
            "limit": 10,
            "offset": 0,
        }
        candidates = {}
        result = requests.post(url, headers=headers, params=params)
        if result.status_code == 200:
            candidates = result.json()['result']['products']
        else:
            print(result.json()['message'])
        return candidates

    '''Добавление продукта к акции'''
    def add_product_to_action(self, action_id, product_id, action_price, stock):
        url = self.url + self.version + "/actions/products/activate"
        params = {
            "action_id": action_id,
            "products": [
                {
                    "action_price": action_price,
                    "product_id": product_id,
                    "stock": stock,
                }
            ]
        }
        headers = self.get_headers()
        products_actions = requests.post(url, headers=headers, params=params)
        return products_actions.json()



