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

# Initializing Twarc2 as a library
client = Twarc2(bearer_token=bearer_token)
max_results, iter, max_iter = 100, 0, 2

# Replace with what you want to search.
query_elon = '(elonmusk OR "elon musk") -is:retweet -is:reply -is:quote lang:en'
query_tesla = 'tesla -is:retweet -is:reply -is:quote lang:en'
# Search time period.
start_time = '2022-04-24T09:00:00Z'
end_time = '2022-04-24T18:00:00Z'

# Get tweets volume with granularity specified as daily count, hourly count or 15-minute count
counts = client.counts_recent(query=query_tesla, granularity='day')
for count in counts:
    data = count['data']
    break
print(json.dumps(data, indent=2))
day, tweet_counts = [], []
for d in data:
    # Add the start date to display on x-axis
    day.append(d['start'][:10])
    # Add the daily Tweet counts to display on the y-axis
    tweet_counts.append(d['tweet_count'])
# Build a bar chart
fig = go.Figure(data=[go.Bar(x=day, y=tweet_counts)])
# Add the titles
fig.update_layout(xaxis_title="Time Period", yaxis_title="Tweet Counts",
                  title_text='Tweets by day for {}'.format(query_tesla))
fig.show()