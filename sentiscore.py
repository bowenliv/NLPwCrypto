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

stopwords_file = "mallet_en_stoplist.txt"
input_file = "rawdata/Tesla_combined_csv.csv"
tesla_bigram = "rawdata/bigram_tesla.csv"
topN_to_show = 50

# function to print sentiments of the sentence.
def sentiment_scores(sentence):
# Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()
# polarity_scores method of SentimentIntensityAnalyzer
# oject gives a sentiment dictionary.
# which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)
    print("Overall sentiment dictionary is : ", sentiment_dict)
    print("sentence was rated as ", sentiment_dict['neg']*100, "% Negative")
    print("sentence was rated as ", sentiment_dict['neu']*100, "% Neutral")
    print("sentence was rated as ", sentiment_dict['pos']*100, "% Positive")
    print("Sentence Overall Rated As", end = " ")
    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05 :
        print("Positive")
    elif sentiment_dict['compound'] <= - 0.05 :
        print("Negative")
    else :
        print("Neutral")


def read_and_clean_lines(infile):
    print("\nReading and cleaning text from {}".format(infile))
    data = pd.read_csv(infile)
    df = pd.DataFrame(data["tweet_text"])
    return (df)

def load_stopwords(filename):
    # ASSIGNMENT: Done
    stopwords = []
    with open(filename, 'rt') as stoplist:
        for line in tqdm(stoplist):
            stopwords += line.split()
    return set(stopwords)


def ngrams(tokens, n):
    # Returns all ngrams of size n in sentence, where an ngram is itself a list of tokens
    ngram = []
    if tokens:
        for i in range(0, len(tokens) - n + 1):
            ngram.append(tokens[i: i + n])
    return ngram

def filter_punctuation_bigrams(ngrams):
    # Input: assume ngrams is a list of ['token1','token2'] bigrams
    # Removes ngrams like ['today','.'] where either token is a single punctuation character
    # Note that this does not mean tokens that merely *contain* punctuation, e.g. "'s"
    # Returns list with the items that were not removed
    punct = string.punctuation
    return [ngram for ngram in ngrams if ngram[0] not in punct and ngram[1] not in punct]

def filter_stopword_bigrams(ngrams, stopwords):
    # Input: assume ngrams is a list of ['token1','token2'] bigrams, stopwords is a set of words like 'the'
    # Removes ngrams like ['in','the'] and ['senator','from'] where either word is a stopword
    # Returns list with the items that were not removed

    return [ngram for ngram in ngrams if ngram[0] not in stopwords and ngram[1] not in stopwords]
    # ASSIGNMENT: Replace this line with your code.

def normalize_tokens(tokenlist):
    # Input: list of tokens as strings,  e.g. ['I', ' ', 'saw', ' ', '@psresnik', ' ', 'on', ' ','Twitter']
    # Output: list of tokens where
    #   - All tokens are lowercased
    #   - All tokens starting with a whitespace character have been filtered out
    #   - All handles (tokens starting with @) have been filtered out
    #   - Any underscores have been replaced with + (since we use _ as a special character in bigrams)

    normalized_tokens = []
    for words in tokenlist:
        if ' ' not in words and '@' not in words:
            normalized_tokens.append(words.lower())
    normalized_tokens = [i.replace('_', '+') for i in normalized_tokens]
    return normalized_tokens

def collect_bigram_counts(lines, stopwords, remove_stopword_bigrams=False):
    # Input lines is a list of raw text strings, stopwords is a set of stopwords
    #
    # Create a bigram counter
    # For each line:
    #   Extract all the bigrams from the line
    #   If remove_stopword_bigrams is True:
    #     Filter out any bigram where either word is a stopword
    #   Increment the count for each bigram
    # Return the counter
    #
    # In the returned counter, the bigrams should be represented as string tokens containing underscores.
    #
    if (remove_stopword_bigrams):
        print("Collecting bigram counts with stopword-filtered bigrams")
    else:
        print("Collecting bigram counts with all bigrams")

    # Initialize spacy and an empty counter
    print("Initializing spacy")
    nlp = English(parser=False)  # faster init with parse=False, if only using for tokenization
    counter = Counter()
    count_list = []
    # Iterate through raw text lines
    for line in tqdm(lines):
        # ASSIGNMENT: placeholder for your code
        doc = nlp(line)
        # Normalize
        list_of_strings = [token.text for token in doc]
        norm_doc = normalize_tokens(list_of_strings)

        # Get bigrams
        bi_gram = ngrams(norm_doc, 2)

        # Filter out bigrams where either token is punctuation
        fp_bigram = filter_punctuation_bigrams(bi_gram)

        # Optionally filter bigrams where either word is a stopword
        if remove_stopword_bigrams == True:
            rs_bigram = filter_stopword_bigrams(fp_bigram, stopwords)

        # Increment bigram counts
        for words in rs_bigram:
            biwords = words[0] + '_' + words[1]
            count_list.append(biwords)
        counter = Counter(count_list)

    return counter


def print_sorted_items(outfile, dict, n=10, order='ascending'):
    if order == 'descending':
        multiplier = -1
    else:
        multiplier = 1
    csvFile = open(outfile, 'w', newline='')
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(['key', 'value'])
    ranked = sorted(dict.items(), key=lambda x: x[1] * multiplier)
    for key, value in ranked[:n]:
        print(key, value)
        csvWriter.writerow([key, value])

tweets = read_and_clean_lines(input_file)
stopwords = load_stopwords(stopwords_file)
print("\nGetting tesla unigram and bigram counts")
tesla_bigram_counts = collect_bigram_counts(tweets['tweet_text'], stopwords, True)
print("\nTop tesla bigrams by frequency")
print_sorted_items(tesla_bigram, tesla_bigram_counts, topN_to_show, 'descending')