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