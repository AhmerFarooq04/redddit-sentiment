import csv
import pandas as pd
import re
import nltk 
from nltk.sentiment.vader import SentimentIntensityAnalyzer

csv_file = 'nasdaq-listed.csv'
csv_file_2 = 'reddit.csv'
symbols = []

with open(csv_file, mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        symbols.append(row['Symbol'])

df = pd.read_csv(csv_file_2)
df_fil = df[['selftext']]
df_fil = df_fil.dropna()

all_tickers = {}
hot_tickers = {}

for symbol in symbols:
    ticker = symbol
    all_tickers[ticker] = 1
  

text_list = df_fil['selftext'].tolist()

pattern = r'\b([A-Z]+)\b'
for string in text_list:
    for word in re.findall(pattern,string):
        if word in all_tickers:
            if word not in hot_tickers:
                hot_tickers[word] = 1
            else:
                hot_tickers[word] += 1

series = pd.Series(hot_tickers).sort_values(ascending = False)

sentiment = {}
final = {}

nltk.download('vader_lexicon')

vader = SentimentIntensityAnalyzer()

for string in text_list:
    for word in re.findall(pattern,string):
        if word in all_tickers:
            score = vader.polarity_scores(string)
            if word not in sentiment:
                sentiment[word] = score
            else:
                for key,i in score.items():
                    sentiment[word][key] += score[key]


compound_values = {ticker: data['compound'] for ticker, data in sentiment.items()}
df_compound = pd.DataFrame(list(compound_values.items()), columns=['Ticker', 'Compound'])
df_compound = df_compound.sort_values(by='Compound', ascending=False)
print(series)
print(df_compound)