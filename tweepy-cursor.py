import tweepy
import json
import tweepy_credentials
from textblob import TextBlob
import datetime
from time import sleep

def get_tweets(crypto):
	auth = tweepy.OAuthHandler(tweepy_credentials.CONSUMER_KEY, tweepy_credentials.CONSUMER_SECRET)
	auth.set_access_token(tweepy_credentials.ACCESS_TOKEN, tweepy_credentials.ACCESS_TOKEN_SECRET)
	api = tweepy.API(auth,wait_on_rate_limit=True)

	now = datetime.datetime.now()
	today = now.date()
	yesterday = today - datetime.timedelta(days=1)
	last_week = today - datetime.timedelta(weeks=1) 

	directory = "tweets/"
	tweets_json = {}
	tweets_json["tweet"] = []
	i=1

	# Arrays with i=0 the query and i=1 the filename
	btc = ["btc OR bitcoin", "btc"]
	bth = ["bth OR bitcoin cash", "bth"]
	eth = ["ethereum OR eth", "eth"]
	etc = ["ethereum classic OR etc", "etc"]
	zrx = ["0x OR zrx", "zrx"]
	ltc = ["litecoin OR ltc", "ltc"]

	if crypto == "btc":
		query = btc
	elif crypto == "bth":
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

	search = tweepy.Cursor(api.search,q=query[0],count=100,
			                           lang="en",
			                           since=str(last_week), until=str(yesterday),
			                           wait_on_rate_limit=True,
			                           wait_on_rate_limit_notify=True).items(16000)

	with open (directory + query[1] + ".json", "w") as f:
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
			print("Query: " + str(query[0]) + " completed.")
			json.dump(tweets_json, f, sort_keys=True, default=str, indent=2)
			print(datetime.datetime.now() - now)
		except tweepy.TweepError:
			time.sleep(60*15)
		except StopIteration:
			print("Exception thrown: StopIteration")

def get_tweet_sentiment(crypto):
	directory = "tweets/"
	query_hits = 0
	query_sentiment_sum = 0
	with open(directory + crypto + ".json") as file:
		data = json.load(file)
		for tweet in data["tweet"]:
			query_hits += 1
			query_sentiment_sum += float(tweet["Sentiment"])
	if query_hits == 0:
		result = 0;print("\n0 hits for the given query")
	else:
		result = round(query_sentiment_sum / query_hits, 4)
	return result

crypto = "ltc"
get_tweets(crypto)
print(get_tweet_sentiment(crypto))