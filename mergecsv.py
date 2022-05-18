import os
import glob
import pandas as pd

extension = 'csv'
all_filenames = [i for i in glob.glob('newdata/combine_*.{}'.format(extension))]
#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
#export to csv
combined_csv.to_csv("newdata/combined_csv.csv", index=False, encoding='utf-8-sig')

# file = ['rawdata/Tesla_labeledV3.csv', 'rawdata/Elon_labeledV3.csv']
# combine_csv = pd.concat([pd.read_csv(f) for f in file])
# print(len(combine_csv))
# new_combine = combine_csv.drop_duplicates(subset=['tweet_text'])
# print(len(new_combine))
# new_combine.to_csv('rawdata/combine_labeledV3.csv', index=False)