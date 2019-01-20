import json, gdax, cryptocompare, requests, csv, pandas as pd, datetime


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
min_order = 2


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
            print_template("I found your crypto price. {} is {} {} at the moment".format(crypto_name, response[currency], currency))
        else:
            print_template("Never heard of {}".format(crypto_name))
        template_crypto_price()


def recommendation_main(crypto):
    #TODO process crypto
    recommendation = {}
    recommendation['main'] = -0.7
    recommendation['news'] = -0.8
    recommendation['price'] = 0.2
    return recommendation


def template_sell():
    account_response = gdax.get_account_balance()
    print(yellow_color("===="))
    crypto_to_sell = []
    for currency_detail in account_response:
        if (float(currency_detail['balance']) > 0 and currency_detail['currency'] != 'EUR'):
            crypto_to_sell.append(currency_detail['currency'])
            print("Currency: {}".format(currency_detail['currency']))
            print("Balance: {}".format(currency_detail['balance']))
            print(yellow_color("===="))
    crypto = input_template(
        "Please choose one of the above Crypto Currencies you'd like to sell. you can only sell all of its balance. or 'menu' to go back to main menu").upper()

    #choosing menu
    if ("MENU" in str(crypto)):
        template_would_you_like()

    #check valid crypto
    if (crypto not in crypto_to_sell):
        print_template("invalid crypto to sell")
        template_sell()
    #if valid then get the balance
    else:
        account_response = gdax.get_account_balance()
        for currency_detail in account_response:
            if (currency_detail['currency'] == crypto):
                balance = round(float(currency_detail['balance']), 8)

    # show current crypto price
    response = cryptocompare.crypto_price(crypto)
    if (response != False):
        priceatm = response[currency]

    follow_confirmation = input_template("are you sure to sell {} of {} with the current price {} {}/{}?".format(balance, crypto, priceatm, crypto, currency))

    if ("yes" in str(follow_confirmation)):
        # TODO remove only specific crypto
        gdax.remove_orders()
        #sell the crypto
        gdax.set_order(crypto, balance, False)
        #logging
        fiat_size = float(priceatm)*balance
        logging(False, crypto, priceatm, balance, fiat_size)
        print_template("Congrats {}, you just sold them all!".format(gdax.get_user_name()))


def template_buy():
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
        template_buy()

    # show current euro balance
    account_response = gdax.get_account_balance()
    for currency_detail in account_response:
        if (currency_detail['currency'] == 'EUR'):
            current_euro = currency_detail['available']
            print_template("Your current balance is {} {}".format(current_euro, currency))

    # show current crypto price
    response = cryptocompare.crypto_price(crypto)
    if (response != False):
        priceatm = response[currency]
        print_template(
            "Current price is {} {} / {} right now".format(response[currency], currency, crypto))

    size = input_template("How much in {} would you like to trade to {}? The minimum order is {} {}".format(currency, crypto, min_order, currency))

    try:
        current_euro = float(current_euro)
        size = float(size)
    except ValueError:
        print_template("Crypto {} is not one of the available crypto to trade".format(crypto))
        template_buy()

    #check minimum order
    if (size <= min_order):
        print_template(yellow_color("Your order is bellow the minimum, please try to make a valid order again"))
        template_buy()

    #check enough credit
    if (size > current_euro):
        print_template(yellow_color("Unfortunately you don't have enough credits, please try to make a valid order again"))
        template_buy()

    #calculate size to buy
    size_crypto_to_buy = round(size/priceatm, 8)

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

    follow = input_template("Do you want to follow our recommendation? say {} to {}follow, or 'no' to {}follow".format(yellow_color("'buy'"), recommendation_yes, recommendation_no))

    if ("buy" in str(follow)):

        follow_confirmation = input_template("Are you sure to {}follow our recommendation buying {} {} worth {} {} with current price {} {}/{}? {} to execute your order, or 'no' to cancel".format(recommendation_yes, size_crypto_to_buy, crypto, size, currency, priceatm, currency, crypto, yellow_color("'yes'"), follow))
        if ("yes" in str(follow_confirmation)):
            #buy
            print_template("Thank you for {}following our recommendation to buy {} {}".format(recommendation_yes, size_crypto_to_buy, crypto))
            order_result = gdax.set_order(crypto, size_crypto_to_buy, True)

            # check if buying success
            if (recommendation_yes == 'not '):
                recommendation_bool = 0
            else:
                recommendation_bool = 1

            if (order_result == True):
                # logging
                logging(True, crypto, priceatm, size_crypto_to_buy, size, recommendation_bool)
                print_template("Congrats {}, your order has been executed".format(gdax.get_user_name()))
            else:
                print_template("Your order is failed due to {}".format(order_result))
            template_would_you_like()
        else:
            print_template(yellow_color('Your order has been cancelled'))
            template_buy()
    else:
        print_template(yellow_color('Your order has been cancelled'))
        template_buy()


def logging(is_buy, crypto, price, size, fiat_size, recommendation_yes=''):
    now = datetime.datetime.now()
    if (is_buy):
        buffer = [[str(crypto), str(size), str(fiat_size), str(recommendation_yes), str(now), str(price)]]
    else:
        buffer = [[str(crypto), str(size), str(fiat_size), str(now), str(price)]]

    for row_index, list in enumerate(buffer):
        for column_index, string in enumerate(list):
            buffer[row_index][column_index] = buffer[row_index][column_index].replace('\n', '')

    if (is_buy):
        filename = 'history_buy.csv'
    else:
        filename = 'history_sell.csv'

    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(buffer)


def template_history():
    print_template("Here is your buying history:")
    buy_history = pd.read_csv("history_buy.csv")
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(buy_history)

    print_template("Here is your selling history:")
    sell_history = pd.read_csv("history_sell.csv")
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(sell_history)
    template_would_you_like()


def template_account_balance():
    print_template("Here is your balance details:")
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
    option = input_template("Would you like to 'buy', 'sell', 'check price', 'check balance', 'history', 're-register' or 'quit' ?")
    if ("price" in str(option)):
        template_crypto_price()
    elif ("history" in str(option)):
        template_history()
    elif ("balance" in str(option)):
        template_account_balance()
        template_would_you_like()
    elif ("buy" in str(option)):
        template_buy()
        main_function()
    elif ("sell" in str(option)):
        template_sell()
        main_function()
    elif ("register" in str(option)):
        template_registration()
    elif("quit" in str(option)):
        print_template("Thank you for using {}. Bye for now {}!".format(system_name,gdax.get_user_name()))
        exit()
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
        print_template("Hi there, welcome to {} The Crypto Currency Personal Assistant. You don't have a valid registered account details yet".format(system_name))
    main_function()

#TODO update when the order is sold server
#TODO simulation
#TODO give recommendation when to sell, if not allow to buy
#TODO logging only when success