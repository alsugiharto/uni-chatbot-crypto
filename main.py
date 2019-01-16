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


available_crypto = {
    'BTC': 'bitcoin',
    'BCH': 'bitcoin cash',
    'ETH': 'ethereum',
    'ETC': 'ethereum classic',
    'ZRX': '0x',
    'LTC': 'litecoin'
}


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
    crypto_name = input_template("What crypto (short name) do you want to know? or say 'menu' to return to menu")
    if ("menu" in str(crypto_name)):
        template_would_you_like()
    else:
        response = cryptocompare.crypto_price(crypto_name)
        if(response != False):
            print_template("I found your crypto price. {} is {} {} at the moment.".format(crypto_name, response[currency], currency))
        else:
            print_template("Never heard of {}.".format(crypto_name))
        template_crypto_price()


def recommendation_main(crypto):
    #TODO process crypto
    recommendation = {}
    recommendation['main'] = -0.7
    recommendation['news'] = -0.8
    recommendation['price'] = 0.2
    return recommendation


def template_trade():
    for symbol in available_crypto:
        print_template("{} ({}) ".format(symbol, available_crypto[symbol]))
    crypto = input_template("Please choose one of the above Crypto Currencies you'd like to trade or 'menu' to go back to main menu").upper()

    #choosing menu
    if ("MENU" in str(crypto)):
        template_would_you_like()

    #check valid crypto
    try:
        available_crypto[crypto]
    except KeyError:
        print_template("Crypto {} is not one of the available crypto to trade".format(crypto))
        template_trade()

    #analyzing for recommendation
    recommendation = recommendation_main(crypto)

    print_template("Alright, after analyzing the current news and prices of {} ({}), we recommend you...".format(available_crypto[crypto], crypto))
    if (recommendation['main'] > 0):
        print_template(yellow_color("to buy with certainty of {} %".format(int(recommendation['main']*100))))

    else:
        print_template(yellow_color("to not buy with certainty of {} %".format(int(recommendation['main'] * 100 * -1))))

    print_template("because currently...")

    if recommendation['price'] >= 0.6:
        price_level = 'super low'
    elif recommendation['price'] >= 0.3:
        price_level = 'quite low'
    elif recommendation['price'] >= 0:
        price_level = 'a lil low'
    elif recommendation['price'] <= -0.6:
        price_level = 'damn high'
    elif recommendation['price'] <= -0.3:
        price_level = 'quite high'
    elif recommendation['price'] < 0:
        price_level = 'a lil high'


    if recommendation['news'] >= 0.6:
        news_level = 'super great'
    elif recommendation['news'] >= 0.3:
        news_level = 'quite good'
    elif recommendation['news'] >= 0:
        news_level = 'a lil oke'
    elif recommendation['news'] <= -0.6:
        news_level = 'super bad'
    elif recommendation['news'] <= -0.3:
        news_level = 'quite bad'
    elif recommendation['news'] < 0:
        news_level = 'a lil not oke'

    if (recommendation['main']>=0):
        #recommendation
        recommendation_yes = ''
        recommendation_no = 'not '
        #choose conjuction
        if (recommendation['price'] >= 0 and recommendation['news'] >= 0):
            conjunction = 'and'
        elif (recommendation['price'] < 0 and recommendation['news'] >= 0):
            conjunction = 'despite'
        elif (recommendation['price'] >= 0 and recommendation['news'] < 0):
            conjunction = 'but luckily'
    else:
        #recommendation
        recommendation_yes = 'not '
        recommendation_no = ''
        # choose conjuction
        if (recommendation['price'] < 0 and recommendation['news'] < 0):
            conjunction = 'and'
        elif (recommendation['price'] < 0 and recommendation['news'] >= 0):
            conjunction = 'but'
        elif (recommendation['price'] >= 0 and recommendation['news'] < 0):
            conjunction = 'despite'


    print_template("the news of {} is {} ({} %)".format(crypto, news_level, int(recommendation['news']*100)))
    print_template("{}..".format(conjunction))
    print_template("the price of {} is {} ({} %)".format(crypto, price_level, int(recommendation['price']*100)))

    follow = input_template("Do you want to follow our recommendation? say 'buy' to {}follow otherwise to {}follow".format(recommendation_yes, recommendation_no))

    if ("buy" in str(follow)):

        #TODO ask how much
        

        follow_confirmation = input_template("Are you sure to buy? 'yes' to execute your order or otherwise to cancel".format(follow))
        if ("yes" in str(follow_confirmation)):
            #TODO buying
            print('buying')
            #TODO logging
            print('logging')
        else:
            print_template(yellow_color('Your order has been cancelled'))
            template_trade()
    else:
        print_template(yellow_color('Your order has been cancelled'))
        template_trade()



def template_account_balance():
    print("{}: Here is your balance details".format(system_name))
    print(yellow_color("===="))
    account_response = gdax.get_account_balance()
    for currency_detail in account_response:
        if (float(currency_detail['balance']) > 0 ):
            print("Currency: {}".format(currency_detail['currency']))
            print("Balance: {}".format(currency_detail['balance']))
            print("Hold: {}".format(currency_detail['hold']))
            print("Available: {}".format(currency_detail['available']))
            print(yellow_color("===="))


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

    main_function()


def template_would_you_like():
    option = input_template("Would you like to 'trade', 'check price', 'check balance', 're-register' or 'quit' ?")
    if ("trade" in str(option)):
        template_trade()
        main_function()
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
        option = input_template("You don't have a valid registered account details yet. choose 'register', otherwise quit")
        if ("register" in str(option)):
            template_registration()


if __name__ == '__main__':
    if (gdax.is_account_valid() == True):
        print_template("Hi {}, welcome to {} The Crypto Currency Personal Assistant".format(gdax.get_user_name(), bold_color(system_name_no_color)))
        template_would_you_like()
    else:
        print_template("Hi there, welcome to {} The Crypto Currency Personal Assistant. You don't have a valid registered account details yet.".format(system_name))
    main_function()


#TODO complete buying
#TODO history
#TODO simulation