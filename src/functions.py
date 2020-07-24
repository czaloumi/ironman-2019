# Plots gender rank 

def plot_genders_rank(sport, df1=fem_pro, df2=male_pro):
    xf = df1['Division Rank']
    yf = df1[sport]
    xm = df2['Division Rank']
    ym = df2[sport]

    fig, ax = plt.subplots(figsize=(10,6))
    ax.scatter(xf, yf, c='pink')
    ax.scatter(xm, ym)

    ax.set_title(f'{sport} Times by Ranking')
    ax.set_xlabel('Division Rank')
    ax.set_ylabel(f'{sport} Time (minutes)')

    ax.axvline(1, c='pink', linestyle="--")
    ax.axvline(xf.max(), c='pink', linestyle="--")
    ax.axvline(1, c='grey', linestyle="--")
    ax.axvline(xm.max(), c='grey', linestyle="--")
    return fig, ax

def scatterplot(sport, div, df=results_df):
    '''
    Parameters:
    sport: str ('Swim', 'Bike', 'Run', 'Overall')
    div: str ('FPRO', 'MPRO', 'F18-24')
    df=results_df: Pandas DataFrame of original data (cleaned)
    
    Returns:
    scatter plot
    '''
    if 'M%' in div:
        df = df[df['Division'] == div]
    else:
        df = df[df['Division'] == div]
    
    x = df['Division Rank']
    y = df[sport].apply(lambda x: x.total_seconds())
    
    fig, ax = plt.subplots(figsize=(10,6))
    ax.scatter(x, y)
    ax.set_title(f'{div} {sport} Times by Ranking')
    ax.set_xlabel(f'{div} Rank')
    ax.set_ylabel(f'{sport} Time (seconds)')
    ax.set_xlim(-1, x.max()+1)
    ax.axvline(1, c='r')
    ax.axvline(x.max(), c='y')
    
    return fig, ax

def timedeltToSec(df, col):
    for i in len(col)
    return df['col'].apply(lambda x: x.total_seconds())

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

def bootstrap_percentile(df, sport, samples, percent, statistic=np.percentile):
    statistics = []
    for i in range(samples):
        samp = times(df, sport)
        statistics.append(statistic(samp, percent))
    return statistics