import pandas as pd
import numpy as np
import datetime
import pdb

class TimeDateToMinutes(object):
    '''
    Converts timedate columns to timedelta to seconds to minutes.
    '''
    
    def __init__(self, df, col1):
        self.df = df
        self.col1 = col1
        self._timedelt()
        self._seconds()
        self._minutes()
        
    def _timedelt(self):
        '''
        Convert cols to timedelta with units in seconds (timedelta puts in ns)
        '''
        self.df[[self.col1]] = self.df[self.col1].apply(pd.to_timedelta, unit='s')
    
    def _seconds(self):
        '''
        Converts df column from timedelta dtype to seconds
        object1.df['Swim'] = object1.df['Swim'].apply(lambda x: x.total_seconds())
        '''
        #pdb.set_trace()
        self.df[self.col1] = self.df[self.col1].apply(lambda x: x.total_seconds())
    
    def _minutes(self):
        '''
        Converts df column from seconds to minutes
        '''
        self.df[self.col1] = self.df[self.col1].divide(60)


if __name__ == '__main__':
    df = pd.read_csv('../data/cleaned.csv')
    col1 = 'Swim'
    
    df['Swim'] = TimeDateToMinutes(df, col1)
    print(df['Swim'])