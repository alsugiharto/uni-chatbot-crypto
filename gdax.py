import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase

system_name = "Crypto15"


class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or b'').decode()
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest()).decode()

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request


def call_api_request(request, json_request='', delete = False):
    try:
        with open('user_account.json') as json_data:
            user_account = json.load(json_data)
        api_url = 'https://api.gdax.com/'
        auth = CoinbaseExchangeAuth(user_account['API_KEY'], user_account['API_SECRET'], user_account['API_PASS'])
        if (delete == True):
            response = requests.delete(api_url + request, auth=auth)
            return response.json()
        elif json_request == '':
            response = requests.get(api_url + request, auth=auth)
            return response.json()
        else:
            response = requests.post(api_url + request, json=json_request, auth=auth)
            return response
    except ValueError:
        return False
    except FileNotFoundError:
        return False


def remove_orders():
    open_orders = call_api_request('orders', '')
    for open_order in open_orders:
        call_api_request('orders/{}'.format(open_order['id']), '', True)


def get_user_name():
    with open('user_account.json') as json_data:
        user_account = json.load(json_data)
    return user_account['NAME']


def is_account_valid():
    valid_response = call_api_request('accounts')
    if(valid_response == False):
        return False
    else:
        try:
            valid_response['message']
            return False
        except TypeError:
            return True


def get_account_balance():
    return call_api_request('accounts')


# market order
def set_order(crypto, size, is_buy):
    if (is_buy):
        buy_sell = 'buy'
    else:
        buy_sell = 'sell'
    json_request = {
        'size': size,
        'type': 'market',
        'side': buy_sell,
        'product_id': '{}-EUR'.format(crypto)
    }
    response = call_api_request('orders', json_request)
    try:
        return response.json()['message']
    except KeyError:
        return True


# market order
def set_stop_order(crypto, size, is_buy, stop_price, limit):
    if (is_buy):
        buy_sell = 'buy'
    else:
        buy_sell = 'sell'

    json_request = {
        'type': 'limit',
        'product_id': '{}-EUR'.format(crypto),
        'size': size,
        'price': limit,
        'stop_price': stop_price,
        'stop': 'loss',
        'side': buy_sell
    }
    response = call_api_request('orders', json_request)
    try:
        return response.json()['message']
    except KeyError:
        return True

def get_order():
    print(call_api_request('orders'))

def products_min_order():
    products = call_api_request('products')
    for product in products:
        if ("EUR" in str(product['id'])):
            print('===')
            print("{}: {}".format(product['id'], product['base_min_size']))