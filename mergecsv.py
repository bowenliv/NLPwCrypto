<<<<<<< HEAD
import os
import glob
import pandas as pd

extension = 'csv'
all_filenames = [i for i in glob.glob('Elon_*.{}'.format(extension))]
#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
#export to csv
=======
import os
import glob
import pandas as pd

extension = 'csv'
all_filenames = [i for i in glob.glob('Elon_*.{}'.format(extension))]
#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
#export to csv
>>>>>>> 886b5665a3becb0dfcfa35c8dd87f5589cd0716f
combined_csv.to_csv( "Elon_combined_csv.csv", index=False, encoding='utf-8-sig')