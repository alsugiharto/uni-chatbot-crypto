import tweepy
import tweepy_credentials
from textblob import TextBlob
from datetime import datetime, timedelta

class TwitterSearch:

	
	def __init__(self):
		pass

	def search_tweet(self, query):
		auth = tweepy.OAuthHandler(tweepy_credentials.CONSUMER_KEY, tweepy_credentials.CONSUMER_SECRET)
		auth.set_access_token(tweepy_credentials.ACCESS_TOKEN, tweepy_credentials.ACCESS_TOKEN_SECRET)

		api = tweepy.API(auth)

		public_tweets = api.search(query, lang  = "en")

		tweet_count = 0
		sentiment_sum = 0

		for tweet in public_tweets:
			# print(tweet.text)
			analysis = TextBlob(tweet.text)
			# print("Sentiment: " + str(round(analysis.sentiment.polarity, 4))
			# 	# + "\nSubjectivity: " + str(round(analysis.sentiment.subjectivity,4)) 
			# 	# + "\nCreated at: " + str(tweet.created_at)
			# 	# + "\nLanguage: " + str(tweet.lang)
			# 	+ "\n<24h?: " + str((datetime.now() -  timedelta(days = 1)) < tweet.created_at)
			# 	# + "\n<1m?: " + str((datetime.now() -  timedelta(minutes = 1)) < tweet.created_at)
			# 	+ "\n\n")
			tweet_count += 1
			sentiment_sum = sentiment_sum + analysis.sentiment.polarity

		# print sentiment average of tweets
		# print("\nAmount of tweets: " + str(tweet_count)
			# + "\nAverage sentiment: " + str(round(sentiment_sum / tweet_count, 4)))
		if tweet_count == 0:
			sentiment = 0
		else:
			sentiment = round(sentiment_sum / tweet_count, 4)
		return sentiment
	
# ts = TwitterSearch()
# ts.search_tweet("btc")