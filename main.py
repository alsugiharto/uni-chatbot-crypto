import json, gdax, cryptocompare, requests

system_name = "Crypto15"
template_menu = " or say 'menu' to return to menu\nYou: "
currency = 'EUR'


def print_template(what_to_say):
    print("{}: {}".format(system_name, what_to_say))


def template_crypto_price():
    crypto_name = input("{}: What crypto do you want to know?{}".format(system_name, template_menu))
    if (crypto_name == 'menu'):
        template_would_you_like()
    else:
        response = cryptocompare.crypto_price(crypto_name)
        if(response != False):
            print_template("I found your crypto price. {} is {} {} at the moment.".format(crypto_name, response[currency], currency))
        else:
            print_template("Never heard of {}.".format(crypto_name))
        template_crypto_price()


def template_trade():
    name = input("{}: What is your name ?\nYou: ".format(system_name))
    api_key = input("{}: What is your api_key ?\nYou: ".format(system_name))
    api_secret = input("{}: What is your api_secret ?\nYou: ".format(system_name))
    api_pass = input("{}: What is your api_pass ?\nYou: ".format(system_name))

    data = {}
    data['API_KEY'] = api_key
    data['API_SECRET'] = api_secret
    data['API_PASS'] = api_pass
    data['NAME'] = name

    with open('user_account.json', 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile)

    main_function()


def template_account_balance():
    # TODO total price in USD
    print("{}: Here is your balance details".format(system_name))
    print("====")
    account_response = gdax.get_account_balance()
    for currency_detail in account_response:
        if (float(currency_detail['balance']) > 0 ):
            print("Currency: {}".format(currency_detail['currency']))
            print("Balance: {}".format(currency_detail['balance']))
            print("Hold: {}".format(currency_detail['hold']))
            print("Available: {}".format(currency_detail['available']))
            print("====")


def template_registration():
    is_registration = input("{}: Do you want to start registration ?\nYou: ".format(system_name))
    if (is_registration == 'yes'):
        name = input("{}: What is your name ?\nYou: ".format(system_name))
        api_key = input("{}: What is your api_key ?\nYou: ".format(system_name))
        api_secret = input("{}: What is your api_secret ?\nYou: ".format(system_name))
        api_pass = input("{}: What is your api_pass ?\nYou: ".format(system_name))

        data = {}
        data['API_KEY'] = api_key
        data['API_SECRET'] = api_secret
        data['API_PASS'] = api_pass
        data['NAME'] = name

        with open('user_account.json', 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile)

        if (gdax.is_account_valid() == True):
            print_template("Congratulation {}, your account is valid!".format(gdax.get_user_name()))
        else:
            print_template("Sorry, but you don't have a valid account details".format(gdax.get_user_name()))

        main_function()
    else:
        main_function()


def template_would_you_like():
    option = input("{}: Would you like to 'trade', 'check price', 'check balance', 're-register' or 'quit' ?\nYou: ".format(system_name))
    if ("trade" in str(option)):
        gdax.set_order()
    elif ("register" in str(option)):
        template_registration()
    elif ("price" in str(option)):
        template_crypto_price()
    elif ("balance" in str(option)):
        template_account_balance()
        template_would_you_like()
    elif("quit" in str(option)):
        print_template("Thank you for using {}. Bye for now {}!".format(system_name,gdax.get_user_name()))
    else:
        print_template("Hmmm sorry {}, what do you mean??".format(gdax.get_user_name()))
        template_would_you_like()


def main_function():
    if (gdax.is_account_valid() == True):
        template_would_you_like()
    else:
        template_registration()


if __name__ == '__main__':
    if (gdax.is_account_valid() == True):
        print_template("Hi {}, welcome to {} The Crypto Currency Personal Assistant".format(gdax.get_user_name(), system_name))
    else:
        print_template("Hi there, welcome to {} The Crypto Currency Personal Assistant. You don't have a valid registered account details yet.".format(system_name))
    main_function()


#TODO history
#TODO simulation