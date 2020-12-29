import pandas as pd
import numpy as np

# After spark import & file is read in as "results_df"

df = results_df.toPandas()

# timecleaning.py class instantiation

from timecleaning import TimeDateToMinutes
object1 = TimeDateToMinutes(df, 'Swim')
object2= TimeDateToMinutes(df, 'Bike')
object3= TimeDateToMinutes(df, 'Run')
object4= TimeDateToMinutes(df, 'Overall')
object5= TimeDateToMinutes(df, 'T1')
object6= TimeDateToMinutes(df, 'T2')

# Convert DNS, DNF, and DQ (disqualified athletes) to 0 & drop 0's
df.loc[df['Division Rank'] == 'DNS', 'Division Rank'] = 0
df.loc[df['Division Rank'] == 'DNF', 'Division Rank'] = 0
df.loc[df['Division Rank'] == 'DQ', 'Division Rank'] = 0
df.loc[df['Overall Rank'] == 'DNS', 'Overall Rank'] = 0
df.loc[df['Overall Rank'] == 'DNF', 'Overall Rank'] = 0
df.loc[df['Overall Rank'] == 'DQ', 'Overall Rank'] = 0

df['Division Rank'] = df['Division Rank'].astype(int)
df['Overall Rank'] = df['Overall Rank'].astype(int)

df.drop(['BIB'],axis=1,inplace=True)
df.dropna(inplace=True)

# Save it!
#df.to_csv('cleaned_data.csv')