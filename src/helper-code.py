# Timedelta to second (before class was built)

def timedeltToSec(df, col):
    for i in len(col)
    return df['col'].apply(lambda x: x.total_seconds())


# Generate random times from df by sport

def times(df, sport):
    '''
    Returns an array of randomly chosen times according to the sport specified.
    
    Parameters:
    df: dataFrame pulling from
    sport: string: 'Swim', 'Bike', 'Run', or 'Overall'
    
    Returns:
    np.array of length 2434, with time entries in seconds
    '''
    l = df[sport]
    return np.random.choice(df[sport], size=len(l), replace=True)


# Generate bootstraps of desired statistic

def bootstrap_statistic(df, sport, samples, statistic):
    '''
    Returns an array of bootstrapped statistics
    
    Parameters:
    df: dataFrame pulling from
    sport: string: 'Swim', 'Bike', 'Run', or 'Overall'
    samples: int: # of samples desired
    statistic: string: statistic to calculate on sample i.e. np.median, np.var, np.std
    '''
    statistics = []
    for i in range(samples):
            samp = times(df, sport)
            statistics.append(statistic(samp))
    return statistics

# Generate specifically bootstrap percentiles

def bootstrap_percentile(df, sport, samples, percent, statistic=np.percentile):
    statistics = []
    for i in range(samples):
        samp = times(df, sport)
        statistics.append(statistic(samp, percent))
    return statistics



# Plots rank vs. standardized event value

def rankvsevent(col1, normalized_sport):
    '''
    Plots athlete's Overall Rank vs. sport time in a bar plot
    '''
    fig, ax = plt.subplots(1, figsize=(12,4))
    
    ax.bar(col1, df[normalized_sport])
    ax.set_title(f'Overall Rank vs. {normalized_sport} Times', fontsize=20)
    ax.set_xlabel(f'Overall Rank', fontsize=15)
    ax.set_ylabel(f'Non Dimensional {normalized_sport} Time')
    return fig, ax


# Define consistency amongst three events

def consistency(row):
    '''
    Returns difference from standardized mean
    '''
    return max(row.Norm_Swim, row.Norm_Run, row.Norm_Bike) - min(row.Norm_Swim, row.Norm_Run, row.Norm_Bike)


# Define specialization in one event

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
    return row[[f'Norm_{other1}', f'Norm_{other2}']].mean() - row[f'Norm_{discipline}']



# Specialize your dataframes

def separate_specialized(df, event, threshold):
    '''
    Returns two dataframes
    
    Parameters:
    df: dataframe
    event: string: event in question
    threshold: float: how specialized do you want to make these athletes?
    
    Returns: 
    spec: df of specialized athletes
    non_spec: df of non specialized athletes
    '''
    spec = df.loc[df[f'Specialize {event}'] > threshold]
    non_spec = df.loc[df[f'Specialize {event}'] < threshold]
    return spec, non_spec