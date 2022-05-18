import csv, re
import os
import sys
import pandas as pd
import codecs
import string
import matplotlib.pyplot as plt
import demoji
import emoji

def read_and_clean_lines(infile):
    print("\nReading and cleaning text from {}".format(infile))
    data = pd.read_csv(infile)
    df = pd.DataFrame(data)
    lines = []
    for line in df['tweet_text']:
        line = line.lower()
        line = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', line)
        # line = line.replace('\'', ' ')
        # line = line.replace('\"', ' ')
        line = line.replace('_', ' ')
        # line = ''.join(line.split('b ', 1))
        # line = re.sub('[\s]+', ' ', line)
        lines.append(line.encode('raw_unicode_escape').decode('unicode_escape').encode('latin1').decode('utf-8'))
    df['tweet_text'] = lines
    return (df)
def swipe_lines(data):
    lines = []
    for line in data:
        line = line.replace('\'', ' ')
        line = line.replace('\"', ' ')
        line = line.replace('-', ' ')
        line = ''.join(line.split('b ', 1))
        line = re.sub('[\s]+', ' ', line)
        lines.append(line)
    return lines

def process_emoji(text):
    emoji_dict = demoji.findall(text)
    # print(emoji_dict)
    for emoji_key, emoji_text in emoji_dict.items():
        text = text.replace(emoji_key, '{' + emoji_text.replace(' ', '_') + '}'+' ')
    return text



def remove_emoji(text):
    dem = demoji.findall(text)
    for item in dem.keys():
        text = text.replace(item, '')
    return text

def unicodetoascii(data):
    TEXTs = []
    for text in data:
        TEXT = (text.
                replace('\\xe2\\x80\\x99', "'").
                replace('\\xc3\\xa9', 'e').
                replace('\\xe2\\x80\\x90', '-').
                replace('\\xe2\\x80\\x91', '-').
                replace('\\xe2\\x80\\x92', '-').
                replace('\\xe2\\x80\\x93', '-').
                replace('\\xe2\\x80\\x94', '-').
                replace('\\xe2\\x80\\x94', '-').
                replace('\\xe2\\x80\\x98', "'").
                replace('\\xe2\\x80\\x9b', "'").
                replace('\\xe2\\x80\\x9c', '"').
                replace('\\xe2\\x80\\x9c', '"').
                replace('\\xe2\\x80\\x9d', '"').
                replace('\\xe2\\x80\\x9e', '"').
                replace('\\xe2\\x80\\x9f', '"').
                replace('\\xe2\\x80\\xa6', '...').
                replace('\\xe2\\x80\\xb2', "'").
                replace('\\xe2\\x80\\xb3', "'").
                replace('\\xe2\\x80\\xb4', "'").
                replace('\\xe2\\x80\\xb5', "'").
                replace('\\xe2\\x80\\xb6', "'").
                replace('\\xe2\\x80\\xb7', "'").
                replace('\\xe2\\x81\\xba', "+").
                replace('\\xe2\\x81\\xbb', "-").
                replace('\\xe2\\x81\\xbc', "=").
                replace('\\xe2\\x81\\xbd', "(").
                replace('\\xe2\\x81\\xbe', ")")
                     )
        TEXTs.append(TEXT)
    return TEXTs

input_file = "newdata/GoldtestdataV2_wemo_.csv"
out_file_wemo = 'newdata/GoldtestdataV2_wemo_.csv'
out_file_woemo = 'newdata/GoldtestdataV2_woemo.csv'

tweets = read_and_clean_lines(input_file)
new_tweets = tweets.drop_duplicates(subset=['tweet_text'])
print('{} tweets before cleaned, {} tweets after cleaned'.format(len(tweets), len(new_tweets)))


# Store data with or without emoji
w_emo, wo_emo = [], []
print('Replacing Emoji to descriptions & Replacing Emoji to blank.')
for tweet in new_tweets['tweet_text']:
    # lines.append(tweet.encode('raw_unicode_escape').decode('unicode_escape').encode('latin1').decode('utf-8'))
    # print(tweet.encode('raw_unicode_escape').decode('unicode_escape').encode('latin1').decode('utf-8')).
    w_emo.append(process_emoji(tweet))
    wo_emo.append(remove_emoji(tweet))
print('****************************************************')
print('Saving describe emoji data.')
w_emo = swipe_lines(w_emo)
new_tweets = new_tweets.assign(tweet_text=w_emo)
print('Replaced emoji with strings: \n{}'.format(new_tweets['tweet_text'][:5]))
new_tweets.to_csv(out_file_wemo, index=False)


print('****************************************************')
print('Saving no emoji data.')
wo_emo = swipe_lines(wo_emo)
new_tweets = new_tweets.assign(tweet_text=wo_emo)
print('Replaced emoji with blanks: \n{}'.format(new_tweets['tweet_text'][:5]))
new_tweets.to_csv(out_file_woemo, index=False, encoding="utf-8")


# new_tweets = tweets.drop_duplicates(subset=['tweet_text'])
# print(len(new_tweets))
# X = (['Raw tweets number', 'Processed tweets number'])
# Y = (tweets.shape[0], new_tweets.shape[0])
# plt.bar(X,Y)
# plt.show()
# print(tweets['tweet_text'].head(5))
# new_tweets.to_csv('newdata/Testdata0516_cleaned_wemo.csv', index=False)