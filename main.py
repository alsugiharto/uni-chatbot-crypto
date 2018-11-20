import json
import requests

def crypto_price(crypto_name):
    crypto_name = crypto_name.upper()
    currency = 'EUR'
    response = requests.get('https://min-api.cryptocompare.com/data/price?fsym={}&tsyms={}'.format(crypto_name, currency)).json()
    try:
        response[currency]
    except KeyError:
        return 'System: Never heard of {}.'.format(crypto_name)
    else:
        return "System: I found your crypto price. {} is {} {} at the moment.".format(crypto_name, response[currency], currency)

if __name__ == '__main__':
    crypto_name = input('System: Hi, What crypto would you like to know the price? \nYou: ')
    while True:
        if crypto_price(crypto_name) != False:
            print(crypto_price(crypto_name))

        crypto_name = input('System: Other crypto? \nYou: ')
