import datetime, requests, talib, api_key, pandas as pd
import numpy as np
from textblob import TextBlob

# Describes the sentiment of their tite and body of 34 different news sources 
# i.e. CryptoGlobe, Coindesk, CoinTelegraph, CryptoInsider

def get_news_sentiment(crypto, days_ago=1):
	btc = ["btc", "bitcoin"]
	bth = ["bth", "bitcoin cash"]
	eth = ["eth", "ethereum"]
	etc = ["etc", "ethereum classic"]
	zrx = ["zrx", "0x"]
	ltc = ["ltc", "litecoin"]

	if crypto == "btc":
		query = btc
	elif crypto =="bth":
		query = bth
	elif crypto == "eth":
		query = eth
	elif crypto == "etc":
		query = etc
	elif crypto == "zrx":
		query = zrx
	elif crypto == "ltc":
		query = ltc
	else:
		query = btc

	url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN" + "&api_key=" + api_key.API_KEY
	response = requests.get(url).json()
	df = pd.DataFrame(response["Data"])

	today = datetime.datetime.now().date()
	d = today - datetime.timedelta(days=days_ago)
	d_in_unix = (datetime.datetime.combine(d, datetime.datetime.min.time()) - datetime.datetime(1970,1,1)).total_seconds()

	# Produce a list containing news objects that are
		# published yesterday or today AND
		# contains the query in the title or categories
	result = []
	for obj in df.values:
		for q in query:
			if obj[7] >= d_in_unix and (q in (obj[0].lower() or obj[1].lower())):
				result.append(obj)
	sentiment = 0
	for article in result:
		sentiment += TextBlob(article[0]).sentiment.polarity
	if len(result) == 0:
		average = 0;
	else:
		average = sentiment / len(result)
	return average