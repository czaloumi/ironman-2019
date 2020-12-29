import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def times(df, sport):
    '''
    Returns an array of randomly chosen times according to the sport specified.
    
    PARAMETERS
    ----------
        df: dataFrame
        sport: string: 'Swim', 'Bike', 'Run', or 'Overall'
    
    RETURNS
    -------
        np.array of randomly chosen time entries in seconds
    '''
    return np.random.choice(df[sport], size=len(df[sport]), replace=True)

def bootstrap_statistic(df, sport, num_samps, statistic):
    '''
    Function generates an array of bootstrapped statistics
    
    PARAMETERS
    ----------
        df: dataFrame 
        sport: string: 'Swim', 'Bike', 'Run', or 'Overall'
        num_samps: int: # of samples desired
        statistic: string: statistic to calculate on sample i.e. np.median, np.var, np.std
    
    RETURNS
    -------
        statistics: list of statistic
    '''
    statistics = []
    for i in range(num_samps):
            samp = times(df, sport)
            statistics.append(statistic(samp))
    return statistics

def bootstrap_difference(df, sport, div1, div2, num_samps, statistic):
    df1 = df[df['Division'] == div1]
    df2 = df[df['Division'] == div2]

    samp1 = bootstrap_statistic(df1, sport, num_samps, statistic)
    samp2 = bootstrap_statistic(df2, sport, num_samps, statistic)

    stats = []
    stats.append(np.array(samp1) - np.array(samp2))
    return stats

def bootstrap_percentile(df, sport, samples, percent, statistic=np.percentile):
    '''
    Function calculates percentiles for a given bootstrapped statistic

    PARAMETERS
    ----------
        df: dataFrame 
        sport: string: 'Swim', 'Bike', 'Run', or 'Overall'
        samples: int: # of samples desired
        statistic: string: statistic to calculate on sample i.e. np.median, np.var, np.std

    RETURNS
    -------
        statistics: list of percentiles
    '''
    statistics = []
    for i in range(samples):
        samp = times(df, sport)
        statistics.append(statistic(samp, percent))
    return statistics

def rankvsevent(col1, normalized_sport):
    '''
    Plots athlete's Overall Rank vs. sport time in a bar plot
    
    PARAMETERS
    ----------
    
    RETURNS
    -------
        None
    '''
    fig, ax = plt.subplots(1, figsize=(12,4))
    
    ax.bar(col1, df[normalized_sport])
    ax.set_title(f'Overall Rank vs. {normalized_sport} Times', fontsize=20)
    ax.set_xlabel(f'Overall Rank', fontsize=15)
    ax.set_ylabel(f'Non Dimensional {normalized_sport} Time')
    return fig, ax

def consistency(row):
    '''
    Returns difference from standardized mean

    PARAMETERS
    ----------
    
    RETURNS
    -------
        
    '''
    return max(row.Norm_Swim, row.Norm_Run, row.Norm_Bike) - min(row.Norm_Swim, row.Norm_Run, row.Norm_Bike)

def specialize(row, discipline):
    '''
    Returns specialize metrics for events (swim, bike, or run)
    Users will need to edit the function to subtract whatever Specialized Metric they are looking for
    specialize('Swim')
    disciplines = [1, 2, 3]

    PARAMETERS
    ----------
    
    RETURNS
    -------
        
    '''
    if discipline == 'Swim':
        other1 = 'Bike'
        other2 = 'Run'
    elif discipline == 'Bike':
        other1 = 'Swim'
        other2 = 'Run'
    else:
        other1 = 'Bike'
        other2 = 'Swim'
    return row[[f'Norm_{other1}', f'Norm_{other2}']].mean() - row[f'Norm_{discipline}']

def separate_specialized(df, event, threshold):
    '''
    Returns two dataframes
    
    PARAMETERS
    ----------
        df: dataframe
        event: string: event in question
        threshold: float: how specialized do you want to make these athletes?
    
    RETURNS
    -------
        spec: df of specialized athletes
        non_spec: df of non specialized athletes
    '''
    spec = df.loc[df[f'Specialize {event}'] > threshold]
    non_spec = df.loc[df[f'Specialize {event}'] < threshold]
    return spec, non_spec

def plot_gender_ranks(axs, df, division='Pro'):
    '''
    Function scatter plots 6 major times in ironman competition by gender:
        Swim, T1, Run, T2, Bike, and Overall
    
    PARAMETERS
    ----------
        ax: axes to plot on
        df: dataframe
        division: string; defaults to pros
            other options: 'Amateur', 'M35-39', 'M30-34', 'M25-29', 'M45-49', 'M40-44',
                           'M18-24', 'M50-54', 'F30-34', 'M55-59', 'F25-29', 'F45-49',
                           'F50-54', 'F35-39', 'F40-44', 'M60-64', 'F18-24', 'F55-59',
                           'M65-69', 'F60-64', 'M70-74', 'F65-69', 'M75-79', 'F70-74',
                           'M80-84'
    
    RETURNS
    -------
        ax
    '''
    female = df[df['Gender'] == 'Female']
    male = df[df['Gender'] == 'Male']
    
    if division == 'Pro':
        female_df = female[female['Division'] == 'FPRO'].copy()
        male_df = male[male['Division'] == 'MPRO'].copy()
    elif division == 'Amateur':
        female_df = female[female['Division'] != 'FPRO'].copy()
        male_df = male[male['Division'] != 'MPRO'].copy()
    else:
        female_df = female[female['Division'] == division].copy()
        male_df = male[male['Division'] == division].copy()
        
    splits = ['Swim', 'T1', 'T2', 'Bike', 'Run', 'Overall']
    
    for time, ax in zip(splits, axs.flatten()):
        x_f = female_df['Division Rank']
        y_f = female_df[time]
        x_m = male_df['Division Rank']
        y_m = male_df[time]
        ax.scatter(x_f, y_f, s=100, c='red', label='Female')
        ax.scatter(x_m, y_m, s=100, label='Male')
        
        ax.axvline(1, c='pink', linestyle="--")
        ax.axvline(x_f.max(), c='pink', linestyle="--")
        ax.axvline(1, c='grey', linestyle="--")
        ax.axvline(x_m.max(), c='grey', linestyle="--")
        
        ax.set_title(f'{division} {time}')
        ax.set_xlabel('Division Rank')
        ax.set_ylabel(f'{time} Time (minutes)')
    
    return ax

def plot_hist_stats(ax, df, sport, div1, div2, num_samps, statistic):
    '''
    Function to plot difference in bootstrapped sample statistics.

    PARAMETERS
    ----------
        ax: axes
        df: dataframe
        sport: string of event ex.) 'Swim', 'T1', 'Bike', 'T2', 'Run', 'Overall'
        div1: string of division/agegroup
        div2: string of second division/agegroup
        num_samps: number of bootstrapped statistics
        statistic: statistic in question ex.) np.mean
    
    RETURNS
    -------
        ax
    '''
    stat_difference = bootstrap_difference(df, sport, div1, div2, num_samps, statistic)

    ax.hist(stat_difference, bins=50)
    ax.set_xlabel(f'{div1} - {div2} Average {sport} Times')
    ax.set_ylabel('Frequency')
    ax.set_title(f'{sport}')