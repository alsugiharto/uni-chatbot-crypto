import api_key, requests, talib, pandas as pd

def get_dataframe(crypto):
	url = "https://min-api.cryptocompare.com/data/histohour?fsym=" + crypto.upper() + "&tsym=EUR&limit=100&e=Coinbase" + "&api_key=" + api_key.API_KEY
	response = requests.get(url).json()
	return pd.DataFrame(response["Data"])

# Relative Strength Index
def get_rsi(df):
	rsi_lst = talib.RSI(df.close.values)
	rsi = round(rsi_lst[len(rsi_lst) - 1],2)
	return conv_rsi(rsi)

def get_macd(df):
	hist = talib.MACD(df.close.values)[2]
	# print(hist)
	hist1 = round(hist[len(hist) - 1], 4)
	hist0 = round(hist[len(hist) - 2], 4)
	# print("Current histogram length: " + str(hist1))
	# print("Previous histogram length: " + str(hist0))
	pos_trend =  hist0 < hist1
	if hist1 > -0.1 and hist1 < 0 and pos_trend:
		result = 1
	elif hist1 < 0.1 and hist1 > 0 and not pos_trend:
		result = -1
	elif not pos_trend:
		result = -0.5
	else:
		result = 0
	return result

# converts the indicator to a number from a -1 to 1 interval
def conv_rsi(indicator, buy=30, sell=70):
	if indicator <= buy:
		result = 1
	elif indicator >= sell:
		result = -1
	else:
		result = 2 * ((indicator - buy) / (sell - buy)) - 1
	return result