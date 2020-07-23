import pandas as pd
import numpy as np

# After spark import & file is read in as "results_df"

df = results_df.toPandas()
df.drop(['BIB'],axis=1,inplace=True)
df.dropna(inplace=True)

# Convert datetime columns to timedelta

cols_to_clean = ['Swim', 'Bike', 'Run', 'Overall', 'T1', 'T2']
df[cols_to_clean] = df[cols_to_clean].apply(pd.to_timedelta, unit='s')

# Convert DNS & DNF to 0 (Did not finish) & convert objects to integers

df.loc[df['Division Rank'] == 'DNS', 'Division Rank'] = 0
df.loc[df['Division Rank'] == 'DNF', 'Division Rank'] = 0
df.loc[df['Division Rank'] == 'DQ', 'Division Rank'] = 0
df['Division Rank'] = df['Division Rank'].astype(int)
df['Overall Rank'] = df['Overall Rank'].astype(int)

# Convert timedelta dtype to seconds

def timedelt_tosec(df, col): 
    '''
    Converts df column from timedelta dtype to seconds
    '''
    return df[col].apply(lambda x: x.total_seconds())

df['Swim'] = timedelt_tosec(df, 'Swim')
df['Bike'] = timedelt_tosec(df, 'Bike')
df['Run'] = timedelt_tosec(df, 'Run')
df['Overall'] = timedelt_tosec(df, 'Overall')
df['T1'] = timedelt_tosec(df, 'T1')
df['T2'] = timedelt_tosec(df, 'T2')
df['Swim'].divide(60)
df['Bike'].divide(60)
df['Run'].divide(60)
df['Overall'].divide(60)
df['T1'].divide(60)
df['T2'].divide(60)

