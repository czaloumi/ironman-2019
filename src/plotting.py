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




# Plot pro 90th Percentiles with 95% CI

def plot_pro_90(sport, df1=fem_pro, df2=male_pro):
    # Generate bootstrap 90th percentiles
    fem_90p = bootstrap_percentile(df1, sport, 1000, 90)
    male_90p = bootstrap_percentile(df2, sport, 1000, 90)
    
    # Say it with confidence
    left_f90p = np.percentile(fem_90p, 2.5)
    right_f90p = np.percentile(fem_90p, 97.5)

    left_m90p = np.percentile(male_90p, 2.5)
    right_m90p = np.percentile(male_90p, 97.5)
    
    # Plot it
    fig, ax = plt.subplots(1, figsize=(12,4))
    ax.hist(fem_90p, bins=50, density=True, color='pink', alpha=0.8, label=f'Female Pro {sport} 90th Percentile')
    ax.hist(male_90p, bins=50, density=True, color='b', alpha=0.7, label=f'Male Pro {sport} 90th Percentile')
    ax.legend()

    ax.set_title(f'Pro {sport} 90th Percentiles', fontsize=20)
    ax.set_xlabel(f'{sport} Time (minutes)', fontsize=15)
    ax.set_ylabel(f'Frequency of Bootstrapped 90th Percentiles', fontsize=10)
    
    ax.axvline(left_f90p, c='pink', linestyle="--")
    ax.axvline(right_f90p, c='pink', linestyle="--")
    ax.axvline(left_m90p, c='grey', linestyle="--")
    ax.axvline(right_m90p, c='grey', linestyle="--")
    
    print(f'Female Pro {sport} Times Bootstrap Confidence Interval for Population 90th Percentile (minutes): [{round(left_f90p, 2)}, {round(right_f90p,2)}]')
    print(f'Male Pro {sport} Times Bootstrap Confidence Interval for Population 90th Percentile (minutes): [{round(left_m90p, 2)}, {round(right_m90p,2)}]')

    return fig, ax




# Plots amateur times with pro 95% CI of 90th percentile

def plot_amateur_proci(sport, df1=fem_agegroups, df2=male_agegroups, df3=fem_pro, df4=male_pro):
    # Convert Amateur times to minutes
    f_agegroups_ = df1[sport]
    m_agegroups_ = df2[sport]

    # Generate pro bootstrap 90th percentiles
    fem_90p = bootstrap_percentile(df3, sport, 1000, 90)
    male_90p = bootstrap_percentile(df4, sport, 1000, 90)
    
    # Say it with confidence
    left_f90p = np.percentile(fem_90p, 2.5)
    right_f90p = np.percentile(fem_90p, 97.5)

    left_m90p = np.percentile(male_90p, 2.5)
    right_m90p = np.percentile(male_90p, 97.5)
    
    # Plot it
    fig, ax = plt.subplots(1, figsize=(12,4))
    
    ax.hist(m_agegroups_, bins=100, density=True, color='grey', alpha=0.75, label=f'Male Amateur {sport} Times')
    ax.hist(f_agegroups_, bins=100, density=True, color='pink', alpha=0.75, label=f'Female Amateur {sport} Times')
    ax.axvline(left_f90p, c='red', linestyle="--", label='Female Pro 90 Percentile')
    ax.axvline(right_f90p, c='red', linestyle="--")
    ax.axvline(left_m90p, c='black', linestyle="--", label='Male Pro 90 Percentile')
    ax.axvline(right_m90p, c='black', linestyle="--")
    ax.legend()

    ax.set_title(f'How do Amateurs Compare to the Pro {sport} 90th Percentile?', fontsize=20)
    ax.set_xlabel(f'{sport} Time (minutes)', fontsize=15)
    ax.set_ylabel('Frequency', fontsize=15)
    
    m_ = m_agegroups_[m_agegroups_ <= right_m90p]
    f_ = f_agegroups_[f_agegroups_ <= right_f90p]
    mam_pros_ = round((len(m_) / len(m_agegroups_))*100, 2)
    fam_pros_ = round((len(f_) / len(f_agegroups_))*100, 2)
    print(f'Percent of male amateurs who {sport} like pros: {mam_pros_}%')
    print(f'Percent of female amateurs who {sport} like pros: {fam_pros_}%')

    return fig, ax




# Plots pro 90th percentile 95% CI with 10th percentile 95% CI

def plot_cis(sport, df1=fem_agegroups, df2=male_agegroups, df3=fem_pro, df4=male_pro):    
    # Bootstrap amateur 10th percentiles
    fem_10 = bootstrap_percentile(df1, sport, 1000, 10)
    male_10 = bootstrap_percentile(df2, sport, 1000, 10)
    
    # Say it with confidence
    left_f10 = np.percentile(fem_10, 2.5)
    right_f10 = np.percentile(fem_10, 97.5)
    left_m10 = np.percentile(male_10, 2.5)
    right_m10 = np.percentile(male_10, 97.5)
    
    # Generate pro bootstrap 90th percentiles
    fem_90 = bootstrap_percentile(df3, sport, 1000, 90)
    male_90 = bootstrap_percentile(df4, sport, 1000, 90)
    
    # Say it with confidence
    left_f90 = np.percentile(fem_90, 2.5)
    right_f90 = np.percentile(fem_90, 97.5)
    left_m90 = np.percentile(male_90, 2.5)
    right_m90 = np.percentile(male_90, 97.5)
    
    # Plot it
    fig, ax = plt.subplots(1, figsize=(12,4))
    
    ax.hist(male_10, bins=100, density=True, color='grey', alpha=0.75, label=f'Male Amateur {sport} 10 Percentiles')
    ax.hist(fem_10, bins=100, density=True, color='pink', alpha=0.75, label=f'Female Amateur {sport} 10 Percentiles')
    ax.axvline(left_f90, c='red', linestyle="--", label='Female Pro 90 Percentile')
    ax.axvline(right_f90, c='red', linestyle="--")
    ax.axvline(left_m90, c='black', linestyle="--", label='Male Pro 90 Percentile')
    ax.axvline(right_m90, c='black', linestyle="--")
    ax.legend()

    ax.set_title(f'How does the {sport} Amateur 10th Percentile Compare to the Pro 90th Percentile?', fontsize=20)
    ax.set_xlabel(f'{sport} Time (minutes)', fontsize=15)

    return fig, ax




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