import csv, re
import os
import sys
import pandas as pd
import codecs


stopwords_file = "mallet_en_stoplist.txt"
input_file = "rawdata/Tesla_combined_csv.csv"
tesla_bigram = "rawdata/bigram_tesla.csv"
topN_to_show = 50

def read_and_clean_lines(infile):
    print("\nReading and cleaning text from {}".format(infile))
    data = pd.read_csv(infile)
    df = pd.DataFrame(data)
    return (df)

def load_stopwords(filename):
    stopwords = []
    with codecs.open(filename, 'r', encoding='ascii', errors='ignore') as fp:
        stopwords = fp.read().split('\n')
    return set(stopwords)

def process_tweet(tweet):
    tweet = str(tweet)
    # Conver to lower case
    tweet = tweet.lower()
    # Convert https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)
    # Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    # Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    # trim
    tweet = tweet.strip()
    # remove last " at string end
    tweet = tweet.rstrip('\'"')
    tweet = tweet.lstrip('\'"')
    return tweet


# end

def uniq(list):
    l = []
    for e in list:
        if e not in l:
            l.append(e)
    return l


# end

def replaceTwoOrMore(s):
    # pattern to look for three or more repetitions of any character, including
    # newlines.
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)

lines = load_stopwords(stopwords_file)
stopWords = []
stopWords.append('AT_USER')
stopWords.append('URL')
for line in lines:
    word = line.strip()
    stopWords.append(word)
feature_vector = []
file2 = 'feature_list.txt'
fp2 = open(file2, 'w')
tweets = read_and_clean_lines(input_file)
count = 0
for row in tweets['tweet_text']:
    tweet = process_tweet(row)
    words = tweet.split()
    count += 1
    print(count)
    for w in words:
        w = replaceTwoOrMore(w)
        w = w.strip('\'"?,.')
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*[a-zA-Z]+[a-zA-Z0-9]*$", w)
        if (w in stopWords or val is None):
            continue
        else:
            feature_vector.append(w.lower())
# endloop
feature_vector = sorted(uniq(feature_vector))
print(feature_vector)
for item in feature_vector:
    fp2.write(item + "\n")

fp2.close()

