import re
import sys
import codecs
import string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
import pandas as pd
import csv


def format_text(myFile):
    replace_no_space = re.compile("[.;:!\'?,\"()\[\]]")
    df = pd.read_csv(myFile)
    all_posts = df['tweet_text']
    labels = df['sentiment_score']

    posts = {}
    posts['positive'] = []
    posts['negative'] = []
    posts['neutral'] = []

    count = 0

    while count < len(all_posts):
        line = all_posts[count].strip()
        post = replace_no_space.sub(" ", line.lower())
        post = post.split()

        if labels[count].lower() == 'positive':
            posts['positive'].append(post)
        elif labels[count].lower() == 'negative':
            posts['negative'].append(post)
        elif labels[count].lower() == 'neutral':
            posts['neutral'].append(post)

        count += 1

    return posts, all_posts, labels


def ngrams(tokens, n):
    ngram = []

    for i in range(len(tokens)):

        if (i + n) <= len(tokens):
            ngram.append(tokens[i:i + n])

    return ngram


def count_ngrams(ngrams_list):
    count = {}

    for i in ngrams_list:

        if i in count.keys():
            count[i] += 1

        else:
            count[i] = 1

    return count


# first: the list for which the sentiment score is needed
# second and third: the lists for the other sentiments
def sentiment_score(first, second, third):
    scores = {}

    for i in first.keys():

        if (i in second) and (i in third):
            scores[i] = first[i] / (second[i] + third[i])
        elif (i in second) and (i not in third):
            scores[i] = first[i] / second[i]
        elif (i not in second) and (i in third):
            scores[i] = first[i] / third[i]
        else:
            scores[i] = 1

    return scores

def IntersecOfSets(arr1, arr2, arr3):
    # Converting the arrays into sets
    s1 = set(arr1)
    s2 = set(arr2)
    s3 = set(arr3)

    # Calculates intersection of
    # sets on s1 and s2
    set1 = s1.intersection(s2)  # [80, 20, 100]

    # Calculates intersection of sets
    # on set1 and s3
    result_set = set1.intersection(s3)

    # Converts resulting set to list
    final_list = list(result_set)
    return final_list

def take_second(elem):
    return elem[1]

def main():
    myFile = open("newdata/labeled.csv", "r")

    posts, all_posts, labels = format_text(myFile)

    temp_lab = posts.keys()

    print("************************************************************************************")
    print("Generating Unigrams")
    print("************************************************************************************")
    tokens = []
    neg_unigrams = []
    pos_unigrams = []
    neu_unigrams = []

    for i in temp_lab:

        for x in posts[i]:

            for y in x:
                tokens.append(y)
                if i == 'negative':
                    neg_unigrams.append(y)

                elif i == 'positive':
                    pos_unigrams.append(y)

                elif i == 'neutral':
                    neu_unigrams.append(y)
    neg_unigrams = sorted(neg_unigrams)
    pos_unigrams = sorted(pos_unigrams)
    neu_unigrams = sorted(neu_unigrams)
    print('Number of negative Unigrams: {}'.format(len(neg_unigrams)))
    print('Number of positive Unigrams: {}'.format(len(pos_unigrams)))
    print('Number of neutral Unigrams: {}'.format(len(neu_unigrams)))
    Common_list = IntersecOfSets(neg_unigrams, pos_unigrams, neu_unigrams)
    Common_list = sorted(Common_list)
    Commonfile = open('gramanalysis/commonlist.txt', 'w')
    for word in Common_list:
        Commonfile.write(str(word) + '\n')
    Commonfile.close()

    # creating the text file with all words and theirs count
    all_counts = count_ngrams(tokens)
    data = open("gramanalysis/uni_count.txt", "w")
    for i in all_counts.keys():
        data.write(i + " " + str(all_counts[i]) + "\n")

    data.close()

    print("\n ************************************************************************************")
    print("Generating Bigrams")
    print("************************************************************************************\n")

    neg_bigrams = []
    pos_bigrams = []
    neu_bigrams = []
    for i in temp_lab:

        for x in posts[i]:

            temp = ngrams(x, 2)

            if i == 'negative':
                for b in temp:
                    neg_bigrams.append(b[0] + " " + b[1])

            elif i == 'positive':
                for b in temp:
                    pos_bigrams.append(b[0] + " " + b[1])

            elif i == 'neutral':
                for b in temp:
                    neu_bigrams.append(b[0] + " " + b[1])

    print("\n ************************************************************************************")
    print("Generating Sentiment Scores for Unigrams")
    print("************************************************************************************\n")

    neg_uni_count = count_ngrams(neg_unigrams)
    pos_uni_count = count_ngrams(pos_unigrams)
    neu_uni_count = count_ngrams(neu_unigrams)

    neg_uni_score = sentiment_score(neg_uni_count, pos_uni_count, neu_uni_count)
    neu_uni_score = sentiment_score(neu_uni_count, pos_uni_count, neg_uni_count)
    pos_uni_score = sentiment_score(pos_uni_count, neg_uni_count, neu_uni_count)

    neg_uni_sent = open("gramanalysis/neg_uni_sent.txt", "w")
    for i in neg_uni_score.keys():
        neg_uni_sent.write(i + " " + str(neg_uni_score[i]) + "\n")

    neg_uni_sent.close()

    neu_uni_sent = open("gramanalysis/neu_uni_sent.txt", "w")
    for i in neu_uni_score.keys():
        neu_uni_sent.write(i + " " + str(neu_uni_score[i]) + "\n")

    neu_uni_sent.close()

    pos_uni_sent = open("gramanalysis/pos_uni_sent.txt", "w")
    for i in pos_uni_score.keys():
        pos_uni_sent.write(i + " " + str(pos_uni_score[i]) + "\n")

    pos_uni_sent.close()

    print("\n ************************************************************************************")
    print("Generating Sentiment Scores for Bigrams")
    print("************************************************************************************\n")

    neg_bi_count = count_ngrams(neg_bigrams)
    pos_bi_count = count_ngrams(pos_bigrams)
    neu_bi_count = count_ngrams(neu_bigrams)

    neg_bi_score = sentiment_score(neg_bi_count, pos_bi_count, neu_bi_count)
    neu_bi_score = sentiment_score(neu_bi_count, pos_bi_count, neg_bi_count)
    pos_bi_score = sentiment_score(pos_bi_count, neg_bi_count, neu_bi_count)

    neg_bi_sent = open("gramanalysis/neg_bi_sent.txt", "w")
    for i in neg_bi_score.keys():
        neg_bi_sent.write(i + " " + str(neg_bi_score[i]) + "\n")

    neg_uni_sent.close()

    neu_bi_sent = open("gramanalysis/neu_bi_sent.txt", "w")
    for i in neu_bi_score.keys():
        neu_bi_sent.write(i + " " + str(neu_bi_score[i]) + "\n")

    neu_bi_sent.close()

    pos_bi_sent = open("gramanalysis/pos_bi_sent.txt", "w")
    for i in pos_bi_score.keys():
        pos_bi_sent.write(i + " " + str(pos_bi_score[i]) + "\n")

    pos_bi_sent.close()


main()


