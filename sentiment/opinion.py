from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import time
analyzer = SentimentIntensityAnalyzer()

pos_count = 0
pos_correct = 0

with open("positive.txt","r") as f:
    for line in f.read().split('\n'):
        vs = analyzer.polarity_scores(line)
        if not vs['neg'] > 0.1:
            if vs['pos']-vs['neg'] > 0:
                pos_correct += 1
            pos_count +=1


neg_count = 0
neg_correct = 0

with open("negative.txt","r") as f:
    for line in f.read().split('\n'):
        vs = analyzer.polarity_scores(line)
        if not vs['pos'] > 0.1:
            if vs['pos']-vs['neg'] <= 0:
                neg_correct += 1
            neg_count +=1

print("Positive accuracy = {}% via {} samples".format(pos_correct/pos_count*100.0, pos_count))
print("Negative accuracy = {}% via {} samples".format(neg_correct/neg_count*100.0, neg_count))

#from transformers import pipeline
# sentiment_pipeline = pipeline("sentiment-analysis")
# data = ["It was the best of times.", "t was the worst of times."]
# sentiment_pipeline(data)
analyzer = SentimentIntensityAnalyzer()

vs = analyzer.polarity_scores("Positive outlook for the future.")
print(vs)
#xd = TextBlob("Many have died.")
#print(xd.sentiment)
#print("\n Neg = {} Neu = {}".format())

# data = {
#     'Date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04'],
#     'SocialMediaPost': ["Great news for the company!", "Mixed opinions on the stock today.", "Positive outlook for the future.", "Stocks are plummeting."],
#     'StockPrice': [100, 105, 110, 95]
# }

# df = pd.DataFrame(data)