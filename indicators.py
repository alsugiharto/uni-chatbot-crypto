import api_key
import requests
import pandas as pd
import talib
import numpy as np

def indicator(crypto):
	df = get_dataframe(crypto)
	rsi = get_rsi(df)
	adx = get_adx(df)
	

def get_dataframe(crypto):
	url = "https://min-api.cryptocompare.com/data/histohour?fsym=" + crypto.upper() + "&tsym=EUR&limit=100&e=Coinbase" + "&api_key=" + api_key.API_KEY
	response = requests.get(url).json()
	return pd.DataFrame(response["Data"])

# Relative Strength Index
def get_rsi(df):
	rsi_lst = talib.RSI(df.close.values)
	return round(rsi_lst[len(rsi_lst) - 1],2)

# Average Directional Movement Index
def get_adx(df):
	adx_lst = talib.ADX(high=df.high.values, low=df.low.values, close=df.close.values, timeperiod=14)
	return round(adx_lst[len(adx_lst) - 1],2)

# converts the indicator to a number from a -1 to 1 interval
def conv_rsi(indicator, buy=30, sell=70):
	mean = abs((buy + sell) / 2)
	result = ((indicator - mean) / (buy - mean))
	if result > 1: result = 1
	elif result < -1: result = -1
	if buy > sell: result = -1 * result
	return round(result, 2)

# converts the indicator to a number from a -1 to 1 interval
# indicators from 0 - 25 are non-existing trends, from 25-100 increasing strength
def conv_adx(indicator):
	if indicator < 25:
		result = 0
	else:
		result = indicator / 100
	return round(result,2)

def interpretation(indicator, value):
	if indicator == "adx":
		if value > 0 and value < 25:
			print("Trend is absent or weak")
		elif value >= 25 and value < 50:
			print("Trend is strong")
		elif value >= 50 and value < 75:
			print("Trend is very strong")
		elif value >= 75 and value <= 100:
			print("Trend is extremely strong")
		else:
			print("Value is out of range 0 - 100")
# print(df)
# print("RSI: " + str(rsi(df)) + "\nConverted: " + str(conv_rsi(rsi(df))))
# print("ADX: " + str(adx(df)) + "\nConverted: " + str(conv_adx(adx(df))))	

# Test Cases
# print("For 0 = buy and 100 = sell")
# r1 = round(np.random.random()*100, 0)
# print("RSI = " + str(r1) +", " + str(conv_rsi(r1, 0, 100)))
# r2 = round(np.random.random()*100, 0)
# print("RSI = " + str(r2) +", " + str(conv_rsi(r2, 0, 100)))
# r3 = round(np.random.random()*-100, 0)
# print("RSI = " + str(r3) +", " + str(conv_rsi(r3, 0, 100)))
# print("RSI = 30, " + str(conv_rsi(30, 0, 100)))
# print("RSI = 70, " + str(conv_rsi(70, 0, 100)))

# print("\nFor 30 = buy and 70 = sell")
# print("RSI = " + str(r1) +", " + str(conv_rsi(r1)))
# print("RSI = " + str(r2) +", " + str(conv_rsi(r2)))
# print("RSI = " + str(r3) +", " + str(conv_rsi(r3)))
# print("RSI = 30, " + str(conv_rsi(30)))
# print("RSI = 70, " + str(conv_rsi(70)))
# # print("RSI = 100, " + str(conv_rsi(100, 0, 100)))
# # print("RSI = 0, " + str(conv_rsi(0, 0, 100)))
# print("\n")
# print("ADX = " + str(r1) + ", " + str(conv_adx(r1)))
# interpretation("adx", r1)
# print("ADX = " + str(r2) +", " + str(conv_adx(r2)))
# interpretation("adx", r2)
# print("ADX = " + str(r3) +", " + str(conv_adx(r3)))
# interpretation("adx", r3)