import tweepy
import json
import tweepy_credentials
# import pandas as pd
# import csv

auth = tweepy.OAuthHandler(tweepy_credentials.CONSUMER_KEY, tweepy_credentials.CONSUMER_SECRET)
auth.set_access_token(tweepy_credentials.ACCESS_TOKEN, tweepy_credentials.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth,wait_on_rate_limit=True)

tweets_json = {}
tweets_json["tweets"] = []
i=1

with open ("tweets.json", "w") as f:
	for tweet in tweepy.Cursor(api.search,q="#btc",count=100,
	                           lang="en",
	                           since="2018-01-05").items():
		textblob = Textblob(tweet.text).sentiment
		tweets_json["tweets"].append({
			"id":			tweet.id
			"Text": 		tweet.text,
			"Created at": 	tweet.created_at,
			"Sentiment": 	textblob.polarity,
			"Subjectivity":	textblob.subjectivity,
		})
		json.dump(tweets_json, f)
		print(str(i) + "/ 180")
		i += 1
