# LAST RUN ON 09-01-2019 11:44
# ERROR 10054, de externe host heeft de verbinding verbroken

import tweepy
import json
import tweepy_credentials
from textblob import TextBlob
import datetime
from time import sleep
# import pandas as pd
# import csv

auth = tweepy.OAuthHandler(tweepy_credentials.CONSUMER_KEY, tweepy_credentials.CONSUMER_SECRET)
auth.set_access_token(tweepy_credentials.ACCESS_TOKEN, tweepy_credentials.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth,wait_on_rate_limit=True)

now = datetime.datetime.now()
today = now.date()
yesterday = today - datetime.timedelta(days=1)
last_week = today - datetime.timedelta(weeks=1) 

tweets_json = {}
tweets_json["tweet"] = []
i=1

bitcoin_query="btc OR bitcoin"
ethereum_query="ethereum OR eth"
litecoin_query = "litecoin OR ltc"
monero_query = "monero OR xmr"
bth_query = "bitcoin cash OR bth"
all_coins = "#btc OR #eth OR #ltc OR #xmr OR bitcoin OR ethereum OR litecoin OR monero"

query = bth_query
search = tweepy.Cursor(api.search,q=query,count=100,
		                           lang="en",
		                           since=str(last_week), until=str(yesterday),
		                           wait_on_rate_limit=True,
		                           wait_on_rate_limit_notify=True).items(16000)

with open ("tweet-bth2.json", "w") as f:
	try:
		for tweet in search:
			textblob = TextBlob(tweet.text).sentiment

			tweets_json["tweet"].append({
				"id":			tweet.id,
				"Text": 		tweet.text,
				"Created at": 	tweet.created_at,
				"Sentiment": 	textblob.polarity,
				"Subjectivity":	textblob.subjectivity,
			})
			print(str(i) + " tweets")
			i += 1
		print("Query: " + query + " completed.")
		json.dump(tweets_json, f, sort_keys=True, default=str, indent=2)
		print(datetime.datetime.now() - now)
	except tweepy.TweepError:
		time.sleep(60*15)
	except StopIteration:
		print("Exception thrown: StopIteration")