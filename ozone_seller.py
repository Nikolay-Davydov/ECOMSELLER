import math
import time
import requests


class OzoneSeller:

    def __init__(self, data):
        self.id = data['id']
        self.key = data['key']
        self.url = data['url']
        self.version = data['version']
        self.repeat = data['repeat']

    def get_headers(self):
        return {
            'Client-id': self.id,
            'Api-Key': self.key,
        }

    def get_actions(self):
        '''Получение всех акций'''
        all_actions = self.do_request('get', '/actions')
        return all_actions

    def get_candidates(self, action_id, limit):
        '''Получение товаров подходящих к акции'''
        result = self.get_candidates_with_offset(action_id, limit, 0)
        total = getattr(result, 'total', 0)
        candidates = getattr(result, 'products', {})
        if total > limit:
            quantity = math.ceil(total / limit)
            page = 1
            while page <= quantity:
                result = self.get_candidates_with_offset(action_id, limit, page * limit + 1)
                candidates.append(getattr(result, 'products', {}))
                page += 1
        return candidates

    def get_candidates_with_offset(self, action_id, limit, offset):
        params = {
            'action_id': action_id,
            'limit': limit,
            'offset': offset,
        }
        result = self.do_request('post', '/actions/candidates', params)
        return result

    def add_product_to_action(self, action_id, product_id, action_price, stock):
        '''Добавление продукта к акции'''
        params = {
            'action_id': action_id,
            'products': [
                {
                    'action_price': action_price,
                    'product_id': product_id,
                    'stock': stock,
                }
            ]
        }
        result = self.do_request('post', '/actions/products/activate', params)
        products_actions = getattr(result, 'product_ids', {})
        return products_actions

    def do_request(self, type_request, type, params=None, repetition=0):
        '''Выполнение запросов'''
        url = self.url + self.version + type
        headers = self.get_headers()
        if type_request == 'get':
            result = requests.get(url, headers=headers)
        else:
            result = requests.post(url, headers=headers, params=params)
        # Рекурсия не самое оптимально решение, применено для минимальной корректировки остального кода
        while result.status_code == 429 and repetition < self.repeat:
            time.sleep(1)
            repetition += 1
            result = self.do_request(type_request, type, params, repetition)
        if result.status_code == 200:
            return result.json()['result']
        else:
            print(result.json()['message'])
            return {}

