from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from textblob import TextBlob

class TelegraphScraper:

	
	def __init__(self):
		pass
	
	# def crypto_lookup(number):
	# 	return {
	# 		"1":"bitcoin",
	# 		"2":"ethereum",
	# 		"3":"altcoin",
	# 		"4":"litecoin",
	# 		"5":"monero",
	# 	}.get(number, "bitcoin")

	# def check_input():
	# 		correct_input = False
	# 		while not correct_input:
	# 			user_input = input("What cryptocurrency are you interested in?\n" +
	# 				"(1) Bitcoin\n" +
	# 				"(2) Ethereum\n" +
	# 				"(3) Altcoin\n" +
	# 				"(4) Litecoin\n" +
	# 				"(5) Monero\n\n" +
	# 				"My choice: ")
	# 			if user_input in ["1", "2", "3", "4", "5"]:
	# 				correct_input = True
	# 			else:
	# 				print("Please enter a number ranging from 1 to 5.\n\n")
	# 		return crypto_lookup(user_input)

	def search_articles(self, query):

		my_url = "https://cointelegraph.com/tags/" + query
		# crypto_choice = check_input()
		# news_url = my_url + query


		# opening up the connection
		uClient = uReq(my_url)
		page_html = uClient.read()
		uClient.close()

		page_soup = soup(page_html, "html.parser")

		containers = page_soup.findAll("article", {"class": "post-preview-item-inline__article"})
		todays_articles = []
		sum_sentiment = 0

		for container in containers:
			date_published = container.find("time", {"class":"post-preview-item-inline__date"}).text.lstrip()
			if "HOUR" in date_published:
				todays_articles.append(container)
				title_container = container.find("span", {"class":"post-preview-item-inline__title"})
				title = title_container.text.lstrip()
				analysis = TextBlob(title)
				sentiment = analysis.sentiment.polarity
				sum_sentiment += sentiment
		articles = len(todays_articles)

		if articles == 0:
			# print("There are no articles about " + query.capitalize() + ".")
			sentiment = 0
		else:
			# print("There are " + str(articles) + " articles today about " + query.capitalize() +".")
			# print("Average sentiment: " + str(round(sum_sentiment / articles, 4)))
			sentiment = round(sum_sentiment / articles, 4)
		return sentiment


# cts = TelegraphScraper()
# cts.search_articles("ethereum")