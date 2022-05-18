import re
import sys
import nltk
import nltk.corpus
from nltk.tokenize import word_tokenize
from tqdm import tqdm
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import spacy
from spacy.lang.en import English
from math import log2
from collections import Counter
import csv
import string
import codecs
import matplotlib.pyplot as plt

# function to print sentiments of the sentence.
def sentiment_scores(sentence):
# Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()
# polarity_scores method of SentimentIntensityAnalyzer
# oject gives a sentiment dictionary.
# which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)
    # print("Overall sentiment dictionary is : ", sentiment_dict)
    # print("sentence was rated as ", sentiment_dict['neg']*100, "% Negative")
    # print("sentence was rated as ", sentiment_dict['neu']*100, "% Neutral")
    # print("sentence was rated as ", sentiment_dict['pos']*100, "% Positive")
    # print("Sentence Overall Rated As", end = " ")
    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05 :
        return("Positive")
    elif sentiment_dict['compound'] <= - 0.05 :
        return("Negative")
    else :
        return("Neutral")

def read_and_clean_lines(infile):
    print("\nReading and cleaning text from {}".format(infile))
    data = pd.read_csv(infile)
    df = pd.DataFrame(data)
    return df

input_file = "newdata/combined_cleaned_wemo_.csv"
output_file = "newdata/labeled_wemo_.csv"

Sentimentvalue = []
tweets = read_and_clean_lines(input_file)
overall_length = len(tweets)
print('reading finished. \n')
# label by VADER
for tweet in tweets['tweet_text']:
    Sentimentvalue.append(sentiment_scores(tweet))
    complete_rate = (len(Sentimentvalue)/overall_length)*100
    print('Dealing with sentiment scores: {} %'.format(round(complete_rate, 2)))
tweets['sentiment_score'] = Sentimentvalue

print('Outputing labeled Data to: \n{}'.format(output_file))
tweets.to_csv(output_file, index=False)
print(tweets['tweet_text'][:10])

P_data = tweets[tweets['sentiment_score']=='Positive']
N_data = tweets[tweets['sentiment_score']=='Negative']
Neu_data = tweets[tweets['sentiment_score']=='Neutral']

# print('Outputing labeled Data by labels. \n')
# P_data.to_csv('newdata/Positive.csv', index=False)
# N_data.to_csv('newdata/Negative.csv', index=False)
# Neu_data.to_csv('newdata/Neutral.csv', index=False)

print('Outputing plot of labels. \n')
X = (['Positive number', 'Neutral number', 'Negative number'])
Y = ([len(P_data), len(Neu_data), len(N_data)])
plt.bar(X, Y)
plt.show()
