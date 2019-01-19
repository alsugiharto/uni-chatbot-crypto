import json
import numpy

bitcoin = ["bitcoin", "btc"]
litecoin = ["litecoin", "ltc"]
ethereum = ["ethereum", "eth"]
monero = ["monero", "xmr"]

crypto_choice = input("Query: ")

def get_list(crypto):
	return {
	"bitcoin": bitcoin,
	"litecoin": litecoin,
	"ethereum": ethereum,
	"monero": monero,
	}.get(crypto, "bitcoin")

query_hits = 0
query_sentiment_sum = 0
with open("tweet-btc.json") as file:
	data = json.load(file)
	for tweet in data["tweet"]:
		for c in get_list(crypto_choice):
			if c in tweet["Text"].lower():
				query_hits += 1
				query_sentiment_sum += float(tweet["Sentiment"])
print("Your query: " + crypto_choice)
print("Amount of hits: " + str(query_hits))
print("Sum of sentiment: " +str(query_sentiment_sum))
if query_hits == 0:
	print("\n0 hits for the given query")
else:
	print("\nMean of sentiment: " + str(round(query_sentiment_sum / query_hits, 4)))

# print(get_list(crypto_choice))
# for c in get_list(crypto_choice):
# 	print(c)
