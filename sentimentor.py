import twitter_sentiment
import cointelegraph_scraper

class Sentimentor:

	
	
	def __init__(self):
		pass

	def crypto_lookup(number):
		return {
			"1":"bitcoin",
			"2":"ethereum",
			"3":"altcoin",
			"4":"litecoin",
			"5":"monero",
		}.get(number, "bitcoin")

	def tui(self):
		correct_input = False
		attempts = 1
		while not correct_input:
			if attempts % 4 != 0:
				user_input = input("What cryptocurrency are you interested in?\n" +
					"(1) Bitcoin\n" +
					"(2) Ethereum\n" +
					"(3) Altcoin\n" +
					"(4) Litecoin\n" +
					"(5) Monero\n\n" +
					"My choice: ")
			else:
				user_input = input("Please enter a number from 1 to 5.\n\nMy choice: ")
			attempts += 1
			
			if user_input in ["1", "2", "3", "4", "5"]:
				correct_input = True
		
		# cryptocurrency = crypto_lookup(user_input)
		cryptocurrency = {
			"1":"bitcoin",
			"2":"ethereum",
			"3":"altcoin",
			"4":"litecoin",
			"5":"monero",
		}.get(user_input, "bitcoin")
		
		ts = twitter_sentiment.TwitterSearch()
		cts = cointelegraph_scraper.TelegraphScraper()
		
		ts_sentiment = ts.search_tweet(cryptocurrency)
		cts_sentiment = cts.search_articles(cryptocurrency)

		ts_weight = 0.67
		cts_weight = 0.33
		
		print("Twitter sentiment: " + str(ts_sentiment)
				+ "\nWeighted: " + str(ts_weight*ts_sentiment) 
				+ "\n\nCointelegraph sentiment: " + str(cts_sentiment)
				+ "\nWeighted: " + str(cts_weight*cts_sentiment)
				+ "\n\nWeighted sentiment: " + str(round((cts_weight*cts_sentiment)+(ts_weight*ts_sentiment),4)))


sentimentor = Sentimentor()
sentimentor.tui()		