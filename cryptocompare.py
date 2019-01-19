import json, gdax, cryptocompare, requests

currency = 'EUR'

def crypto_price(crypto_name):
    crypto_name = crypto_name.upper()
    currency = 'EUR'
    response = requests.get(
        'https://min-api.cryptocompare.com/data/price?fsym={}&tsyms={}&e=Coinbase'.format(crypto_name, currency)).json()
    try:
        response[currency]
    except KeyError:
        return False
    return response

