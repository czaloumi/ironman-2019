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

def plot_percentile(sport, df, division, percentile):
    '''
    Function plots percentiles of athletes for a given sport by gender.
        Note: 90th percentile are SLOWER athletes! 10th percentile are FAST athletes.
    
    PARAMETERS
    ----------
        sport: string; 'Swim', 'T1', Run', 'T2', 'Bike', or 'Overall'
        df: pandas dataframe
        percentile: int; 90 = 90th percentile, 95 = 95th percentile
        
    RETURNS
    -------
        Plot of sport time vs. bootstrapped samples
        CIf: confidence interval list containing lower and upper bounds for female athletes
        CIm: confidence interval list containing lower and upper bounds for male athletes
    '''
    # Separate genders
    fem_df = df[df['Division']==f'F{division}']
    male_df = df[df['Division']==f'M{division}']
    
    # Generate bootstrap percentiles
    fem_percentiles = bootstrap_percentile(fem_df, sport, 1000, percentile)
    male_percentiles = bootstrap_percentile(male_df, sport, 1000, percentile)
    
    # Confidence intervals
    CIf = []
    CIf.append(np.percentile(fem_percentiles, ((100-percentile)/2)))
    CIf.append(np.percentile(fem_percentiles, (percentile + (100-percentile)/2)))
    
    CIm = []
    CIm.append(np.percentile(male_percentiles, ((100-percentile)/2)))
    CIm.append(np.percentile(male_percentiles, (percentile + (100-percentile)/2)))
    
    # Plot
    fig, ax = plt.subplots(1, figsize=(12,4))
    ax.hist(fem_percentiles, density=True, color='pink', alpha=0.8, label=f'Female {division} {sport} {percentile}th Percentile')
    ax.hist(male_percentiles, density=True, color='b', alpha=0.7, label=f'Male {division} {sport} {percentile}th Percentile')
    ax.legend()

    ax.set_title(f'{division} {sport} {percentile}th Percentiles', fontsize=20)
    ax.set_xlabel(f'{sport} Time (minutes)', fontsize=15)
    ax.set_ylabel(f'Frequency of {percentile}th Percentiles', fontsize=10)
    
    ax.axvline(CIf[0], c='pink', linestyle="--")
    ax.axvline(CIf[1], c='pink', linestyle="--")
    ax.axvline(CIm[0], c='grey', linestyle="--")
    ax.axvline(CIm[1], c='grey', linestyle="--")
    
    print(f'Female {division} {sport} Times Bootstrap CI {percentile}th Percentile (minutes): [{round(CIf[0], 2)}, {round(CIf[1],2)}]')
    print(f'Male {division} {sport} Times Bootstrap CI{percentile}th Percentile (minutes): [{round(CIm[0], 2)}, {round(CIm[1],2)}]')

    return fig, ax, CIf, CIm

def plot_fastamateurs(sport, df, samples=1000):
    '''
    Funciton plots 10th percentile amateurs for a given sport 
    and 90th percentile professional athletes.
        Note: 10th percentile = fast & 90th percentile = slow
        
    PARAMETERS
    ----------
        sport: string; 'Swim', 'T1', 'Run', 'T2', 'Bike', 'Overall'
        df: pandas dataframe
        samples: int; number of bootstrapped samples to generate
    
    RETUNRS
    -------
        plot of 10th percentile amateurs and 90th percentile CI for slow professionals
        plot of 90th percentile pros
    '''
    amateur_df = df[(df['Division'] != 'FPRO') & (df['Division'] != 'MPRO')]
    female_df = amateur_df[amateur_df['Division'].str.contains('F')]
    male_df = amateur_df[amateur_df['Division'].str.contains('M')]
    
    fast_fem_amateurs = bootstrap_percentile(female_df, sport, samples, 10, statistic=np.percentile)
    fast_male_amateurs = bootstrap_percentile(male_df, sport, samples, 10, statistic=np.percentile)
    
    fig, _, pro_CIf, pro_CIm = plot_percentile(sport, df, 'PRO', percentile=90)
    plt.close(fig)
    
    fig, ax = plt.subplots(figsize=(12,4))
    ax.hist(fast_fem_amateurs, color='pink', label='F Amateurs')
    ax.hist(fast_male_amateurs, color='b', alpha=0.5, label='M Amateurs')
    ax.axvline(pro_CIf[0], c='r', linestyle='--', label='FPRO 90th Percentile')
    ax.axvline(pro_CIf[1], c='r', linestyle='--')
    ax.axvline(pro_CIm[0], c='black', linestyle='--', label='MPRO 90th Percentile')
    ax.axvline(pro_CIm[1], c='black', linestyle='--')
    ax.set_title(f'Amateur {sport} 10th Percentiles', fontsize=20)
    ax.set_xlabel(f'{sport} Time (minutes)', fontsize=15)
    ax.set_ylabel(f'Frequency', fontsize=10)
    ax.legend()
    return ax

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
    '''
    return max(row.Swim_Scaled, row.Run_Scaled, row.Bike_Scaled) - min(row.Swim_Scaled, row.Run_Scaled, row.Bike_Scaled)


def specialize(row, discipline):
    '''
    Returns specialize metrics for events (swim, bike, or run)
    Users will need to edit the function to subtract whatever Specialized Metric they are looking for
    specialize('Swim')
    disciplines = [1, 2, 3]
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
    return row[[f'{other1}_Scaled', f'{other2}_Scaled']].mean() - row[f'{discipline}_Scaled']

def plot_specialization(df, division):
    '''
    Function scatter plots specialization scores for Swim, BIke, and Run events
    by athlete division rank.
    
    Note: function plots two separate plots per division gender.
    
    PARAMETERS
    ----------
        df: pandas dataframe
        division: string
    
    RETURNS
    -------
        Two plots by division gender
    '''
    female_df = df[df['Gender'] == 0]
    male_df = df[df['Gender'] == 1]
    fem_div = female_df[female_df['Division'] == f'F{division}']
    male_div = male_df[male_df['Division'] == f'M{division}']
    gender_dfs = [male_div, fem_div]
    
    specialization_cols = ['Specialize_Swim', 'Specialize_Bike', 'Specialize_Run']
    
    fig, axs = plt.subplots(2, figsize=(12, 12))
    for i, gender_df in enumerate(gender_dfs):
        if i == 0:
            axs[i].set_title(f'Male {division} Specialization')
        else:
            axs[i].set_title(f'Female {division} Specialization')

        for col in specialization_cols:
            axs[i].scatter(gender_df[col], gender_df['Overall Rank'], label=f'{col}')
        axs[i].set_xlabel('Specialization Score')
        axs[i].set_ylabel('Rank')
        axs[i].set_xbound(-1.5, 1.5)
        axs[0].set_ybound(-5,100)
        axs[i].legend()
    
    return axs

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
    spec = df.loc[df[f'Specialize_{event}'] > threshold]
    non_spec = df.loc[df[f'Specialize_{event}'] < threshold]
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
    female = df[df['Gender'] == 0]
    male = df[df['Gender'] == 1]
    
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