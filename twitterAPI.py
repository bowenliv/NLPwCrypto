<<<<<<< HEAD
import os
import tweepy
import pandas as pd
import csv
import plotly.graph_objects as go
from twarc import Twarc2
import json

consumer_key = 'Wc0zE7bZt19peFp1XFlKoENT0'
consumer_secret = 'UE1gakkF5xYdph0HONzJV7spezipH9b3zqBVhWUUBs6VN5ctBX'
access_token = '1514819434577162247-mAz9UAyCllRtWtwcxw0wIqrNMZzk3d'
access_token_secret = '2TmOzApC8aqoB9ReRDLmseXgX1wpJXkChJ9jRcOrFJsxf'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAACwLbgEAAAAAWT5i7TfYhYCF7VOIaoExvWZXTyc%3DxFN0KL7h3HtQsRWKqYKw0uPBhnjzbWoy285a3ccxZF6IHo8Iv1'

# Twitter authentication and the connection to Twitter API
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
# api = tweepy.API(auth, wait_on_rate_limit=True)

# Initializing Tweepy API
client = tweepy.Client(bearer_token=bearer_token)
# Initializing Twarc2 as a library
# client = Twarc2(bearer_token=bearer_token)

# max_results number must between 10 and 100, select the maximum number of result to search in one time.
# max_iter number controls pa
max_results, iter, max_iter = 100, 0, 30
# Replace with what you want to search.
query_elon = '(elonmusk OR "elon musk") -is:retweet -is:reply -is:quote lang:en'
query_tesla = 'tesla -is:retweet -is:reply -is:quote lang:en'

# Search time period.
start_time = '2022-04-25T08:00:00Z'
end_time = '2022-04-25T16:00:00Z'

# Open/create a file to append data to
csvFile = open('Tesla_0425.csv', 'w', newline='')
# Use csv writer
csvWriter = csv.writer(csvFile)
csvWriter.writerow(['timestamp', 'author_id', 'tweet_text', 'retweet_count', 'reply_count', 'favorite_count',
                    'sentiment_score'])
counter = 0
for iter in range(max_iter):
    response = client.search_recent_tweets(query=query_tesla, max_results=max_results,
                                           tweet_fields=['context_annotations', 'public_metrics', 'created_at'],
                                           start_time=start_time, end_time=end_time, expansions='author_id',
                                           user_fields=['id', 'username', 'public_metrics'])
    # Write a row to the CSV file.
    for tweet in response.data:
        csvWriter.writerow([tweet.created_at, tweet.author_id, tweet.text.replace('\n',' ').encode('utf-8'),
                            tweet.public_metrics['retweet_count'], tweet.public_metrics['reply_count'],
                            tweet.public_metrics['like_count']])
        counter += 1
        print(counter)
    del response
=======
import os
import tweepy
import pandas as pd
import csv
import plotly.graph_objects as go
from twarc import Twarc2
import json

consumer_key = 'Wc0zE7bZt19peFp1XFlKoENT0'
consumer_secret = 'UE1gakkF5xYdph0HONzJV7spezipH9b3zqBVhWUUBs6VN5ctBX'
access_token = '1514819434577162247-mAz9UAyCllRtWtwcxw0wIqrNMZzk3d'
access_token_secret = '2TmOzApC8aqoB9ReRDLmseXgX1wpJXkChJ9jRcOrFJsxf'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAACwLbgEAAAAAWT5i7TfYhYCF7VOIaoExvWZXTyc%3DxFN0KL7h3HtQsRWKqYKw0uPBhnjzbWoy285a3ccxZF6IHo8Iv1'

# Twitter authentication and the connection to Twitter API
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
# api = tweepy.API(auth, wait_on_rate_limit=True)

# Initializing Tweepy API
client = tweepy.Client(bearer_token=bearer_token)
# Initializing Twarc2 as a library
# client = Twarc2(bearer_token=bearer_token)

# max_results number must between 10 and 100, select the maximum number of result to search in one time.
# max_iter number controls pa
max_results, iter, max_iter = 100, 0, 30
# Replace with what you want to search.
query_elon = '(elonmusk OR "elon musk") -is:retweet -is:reply -is:quote lang:en'
query_tesla = 'tesla -is:retweet -is:reply -is:quote lang:en'

# Search time period.
start_time = '2022-04-25T08:00:00Z'
end_time = '2022-04-25T16:00:00Z'

# Open/create a file to append data to
csvFile = open('Tesla_0425.csv', 'w', newline='')
# Use csv writer
csvWriter = csv.writer(csvFile)
csvWriter.writerow(['timestamp', 'author_id', 'tweet_text', 'retweet_count', 'reply_count', 'favorite_count',
                    'sentiment_score'])
counter = 0
for iter in range(max_iter):
    response = client.search_recent_tweets(query=query_tesla, max_results=max_results,
                                           tweet_fields=['context_annotations', 'public_metrics', 'created_at'],
                                           start_time=start_time, end_time=end_time, expansions='author_id',
                                           user_fields=['id', 'username', 'public_metrics'])
    # Write a row to the CSV file.
    for tweet in response.data:
        csvWriter.writerow([tweet.created_at, tweet.author_id, tweet.text.replace('\n',' ').encode('utf-8'),
                            tweet.public_metrics['retweet_count'], tweet.public_metrics['reply_count'],
                            tweet.public_metrics['like_count']])
        counter += 1
        print(counter)
    del response
>>>>>>> 886b5665a3becb0dfcfa35c8dd87f5589cd0716f
