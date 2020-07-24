# T-Tests w/unequal variance 

t_statistic, pvalue = ttest_ind(male_pro['Overall'], fem_pro['Overall'], equal_var=False)
print(f'Pro t-test statistic: {round(t_statistic,2)}')
print(f'Pro p-value: {pvalue}')


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


# Determining who fast amateurs are - pulling names from column
# Generate pro bootstrap 90th percentiles
fem_90p = bootstrap_percentile(fem_pro, 'Overall', 1000, 90)
male_90p = bootstrap_percentile(male_pro, 'Overall', 1000, 90)
    
# Say it with confidence
left_f90p = np.percentile(fem_90p, 2.5)
right_f90p = np.percentile(fem_90p, 97.5)

left_m90p = np.percentile(male_90p, 2.5)
right_m90p = np.percentile(male_90p, 97.5)

m = male_agegroups[male_agegroups.Overall <= right_m90p]
f = fem_agegroups[fem_agegroups.Overall <= right_f90p]
sponsor_these_men = m.sort_values('Overall')['Name'].tolist()
sponsor_these_women = f.sort_values('Overall')['Name'].tolist()

print(f'Best Male Amateurs:')
print(' ')
for i in range(len(sponsor_these_men)):
    print(f'{i} {sponsor_these_men[i]}')
print(' ')
print(f'Best Female Amateurs:')
print(' ')
for i in range(int(len(sponsor_these_women)/5)):
    print(f'{i} {sponsor_these_women[i]}')
    
    
# Standardize event time columns by subtracting mean and dividing by standard deviation:
# Adds new columns for each standardized event time
df['Norm_Swim'] = ( df['Swim'] - np.mean(df['Swim']) ) / np.std(df['Swim'])
df['Norm_Bike'] = ( df['Bike'] - np.mean(df['Bike']) ) / np.std(df['Bike'])
df['Norm_Run'] = ( df['Run'] - np.mean(df['Run']) ) / np.std(df['Run'])
df['Norm_T1'] = ( df['T1'] - np.mean(df['T1']) ) / np.std(df['T1'])
df['Norm_T2'] = ( df['T2'] - np.mean(df['T2']) ) / np.std(df['T2'])


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


# Unique divisions, sorted

male_div_list = male_agegroups.Division.unique()
fem_div_list = fem_agegroups.Division.unique()
f = np.sort(fem_div_list)
m = np.sort(male_div_list)


# Plots specialization by division rank for all female divisions (minus pro)

fig, ax = plt.subplots(len(f), 1, figsize=(12,50))

for i, j in enumerate(f):
    plot_df = fem_results[fem_results['Division'] == f'{j}']

    ax[i].scatter(plot_df['Specialize Swim'], plot_df['Division Rank'], color='aqua', label='Swim')
    ax[i].scatter(plot_df['Specialize Bike'], plot_df['Division Rank'],color='crimson', label='Bike')
    ax[i].scatter(plot_df['Specialize Run'], plot_df['Division Rank'],color='violet', label='Run')
    ax[i].set_title(f'Female {j} Specialization by Rank', fontsize=20)
    ax[i].set_xlabel('Specialization Score', fontsize=12)
    ax[i].set_ylabel('Rank', fontsize=12)
    #ax[i].set_xbound(-1,)
    #ax[i].set_ybound(-1, 100)
    ax[i].legend()
plt.tight_layout()


# same same but for male

fig, ax = plt.subplots(len(m), 1, figsize=(12,50))

for i, j in enumerate(m):
    plot_df = male_results[male_results['Division'] == f'{j}']

    ax[i].scatter(plot_df['Specialize Swim'], plot_df['Division Rank'], color='aqua', label='Swim')
    ax[i].scatter(plot_df['Specialize Bike'], plot_df['Division Rank'],color='red', label='Bike')
    ax[i].scatter(plot_df['Specialize Run'], plot_df['Division Rank'],color='green', label='Run')
    ax[i].set_title(f'Male {j} Specialization by Rank', fontsize=20)
    ax[i].set_xlabel('Specialization Score', fontsize=12)
    ax[i].set_ylabel('Rank', fontsize=12)
    #ax[i].set_xbound(-1,)
    #ax[i].set_ybound(-1, 100)
    ax[i].legend()
plt.tight_layout()


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