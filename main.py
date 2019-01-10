import json, gdax, cryptocompare, requests


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def yellow_color(text):
    return bcolors.WARNING + "{}".format(text) + bcolors.ENDC


def blue_color(text):
    return bcolors.OKBLUE + "{}".format(text) + bcolors.ENDC


def green_color(text):
    return bcolors.OKGREEN + "{}".format(text) + bcolors.ENDC


def bold_color(text):
    return bcolors.BOLD + "{}".format(text) + bcolors.ENDC


system_name_no_color = "Crypto15"
system_name = yellow_color(system_name_no_color)
currency = 'EUR'


def print_template(text):
    print("{}: {}".format(system_name, text))


def input_template(text):
    if(gdax.is_account_valid()):
        name = gdax.get_user_name()
    else:
        name = "You"
    return input("{}: {} \n{}: ".format(system_name, text, blue_color(name)))


def template_crypto_price():
    crypto_name = input_template("What crypto do you want to know? or say 'menu' to return to menu")
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
    name = input_template("What is your name?")
    api_key = input_template("What is your API_KEY?")
    api_secret = input_template("What is your API_SECRET?")
    api_pass = input_template("What is your API_PASS?")

    data = {}
    data['API_KEY'] = api_key
    data['API_SECRET'] = api_secret
    data['API_PASS'] = api_pass
    data['NAME'] = name

    with open('user_account.json', 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile)


def template_account_balance():
    print("{}: Here is your balance details".format(system_name))
    print(green_color("===="))
    account_response = gdax.get_account_balance()
    for currency_detail in account_response:
        if (float(currency_detail['balance']) > 0 ):
            print("Currency: {}".format(currency_detail['currency']))
            print("Balance: {}".format(currency_detail['balance']))
            print("Hold: {}".format(currency_detail['hold']))
            print("Available: {}".format(currency_detail['available']))
            print(green_color("===="))


def template_registration():
    is_registration = input_template("Do you want to start registration?")
    if (is_registration == 'yes'):
        name = input_template("What is your name?")
        api_key = input_template("What is your API_KEY?")
        api_secret = input_template("What is your API_SECRET?")
        api_pass = input_template("What is your API_PASS?")

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


def template_would_you_like():
    option = input_template("Would you like to 'trade', 'check price', 'check balance', 're-register' or 'quit' ?")
    if ("trade" in str(option)):
        gdax.set_order()
        main_function()
    elif ("register" in str(option)):
        template_registration()
        main_function()
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
        print_template("Hi {}, welcome to {} The Crypto Currency Personal Assistant".format(gdax.get_user_name(), bold_color(system_name_no_color)))
    else:
        print_template("Hi there, welcome to {} The Crypto Currency Personal Assistant. You don't have a valid registered account details yet.".format(system_name))
    main_function()


#TODO history
#TODO simulation