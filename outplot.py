import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt

def percent(data):
  values = []
  for value in data.values():
    values.append(100*value/sum(data.values()))
  return values

data = pd.read_csv('newdata/labeled.csv')
wemo = pd.read_csv('newdata/labeled_wemo.csv')
woemo = pd.read_csv('newdata/labeled_woemo.csv')

label_c = Counter(data['sentiment_score'])
wemo_c = Counter(wemo['sentiment_score'])
woemo_c = Counter(woemo['sentiment_score'])

print("Normal label counts:---------{}".format(label_c))
print("With emoji label counts:-----{}".format(wemo_c))
print("Without emoji label counts:--{}".format(woemo_c))

x = np.arange(len(label_c.keys()))
width=0.24
fig, ax= plt.subplots()

rects1 = ax.bar(x - width, sorted(percent(label_c)), width, color='r')
rects2 = ax.bar(x, sorted(percent(wemo_c)), width, color='b')
rects3 = ax.bar(x + width, sorted(percent(woemo_c)), width, color='g')
ax.set_ylabel('Percentage %')
ax.set_title('Number of tweets by label')
ax.legend((rects1[0], rects2[0], rects3[0]), ('Unicode emoji', 'With emoji', 'Without emoji'))
ax.set_xticklabels( ('', 'Negative', '', 'Neutral', '', 'Positive') )
plt.show()