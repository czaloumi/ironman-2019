bootstrap_swim = bootstrap_statistic(df, 'Swim', 10000, np.median)
bootstrap_bike = bootstrap_statistic(df, 'Bike', 10000, np.median)
bootstrap_run = bootstrap_statistic(df, 'Run', 10000, np.median)

fig, ax = plt.subplots(3, 1, figsize=(12,7))

ax[0].hist(bootstrap_swim, bins=25, density=True, color='blue', alpha=0.75, label='Bootstrap Sample Swim Time Medians')
ax[0].hist(times(df, 'Swim'), bins=25, density=True, color="blue", alpha=0.4, label="Sample Swims")
ax[0].set_xbound(3750,5250)
ax[0].set_xlabel('Swim in Seconds', fontsize=15)

ax[1].hist(bootstrap_bike, bins=25, density=True, color='yellow', alpha=0.75, label='Bootstrap Sample Bike Time Medians')
ax[1].hist(times(df, 'Bike'), bins=25, density=True, color="yellow", alpha=0.4, label="Sample Swims")
ax[1].set_xbound(18000, 24000)
ax[1].set_xlabel('Bike in Seconds', fontsize=15)

ax[2].hist(bootstrap_run, bins=25, density=True, color='red', alpha=0.75, label='Bootstrap Sample Run Time Medians')
ax[2].hist(times(df, 'Run'), bins=25, density=True, color="red", alpha=0.4, label="Sample Runs")
ax[2].set_xbound(11000, 19000)
ax[2].set_xlabel('Run in Seconds', fontsize=15)

plt.tight_layout()

fig,ax = plt.subplots(1, figsize=(20,5))

ax.hist(bootstrap_swim, bins=25, density=True, color='blue', alpha = 0.75, label='Bootstrap Sample Swim Time Medians')
ax.hist(times(df, 'Swim'), bins=25, density=True, color="blue", alpha=0.4, label="Sample Swims")

ax.hist(bootstrap_bike, bins=25, density=True, color='yellow', label='Bootstrap Sample Bike Time Medians')
ax.hist(times(df, 'Bike'), bins=25, density=True, color="yellow", alpha=0.4, label="Sample Swims")

ax.hist(bootstrap_run, bins=25, density=True, color='red', label='Bootstrap Sample Run Time Medians')
ax.hist(times(df, 'Run'), bins=25, density=True, color="red", alpha=0.4, label="Sample Runs")

ax.set_title("Bootstrap Sample Medians (10,000 samples)", fontsize = 20)
ax.set_xlabel('Time in Seconds', fontsize=15)
ax.set_xbound(0, 24000)
ax.set_ybound(0, .027)
ax.legend()

fem_pro = df[df['Division'] == 'FPRO']

bootstrap_fpro_swim = bootstrap_statistic(fem_pro, 'Swim', 1000, np.median)

fig, ax = plt.subplots(1, figsize=(12,7))

ax.hist(bootstrap_fpro_swim, bins=25, density=True, color='pink', alpha=0.75, label='Sample Swim Time Medians')
ax.hist(times(fem_pro, 'Swim'), bins=25, density=True, color="pink", alpha=0.4, label="Sample Swims")
ax.set_title('Bootstrap Sample FPRO Swim Medians (1,000 Samples)', fontsize=20)
ax.set_xbound(2500, 4700)
ax.set_xlabel('Swim in Seconds', fontsize=15)
ax.legend()

std_samp = np.std(times(fem_pro, 'Swim'))
std_b_medians = np.std(bootstrap_fpro_swim)
print(f'Standard Deviation of Sample (minutes): {round(std_samp/60, 2)} and standard deviation of sample medians (minutes): {round(std_b_medians/60,2)}')

fem_pro_p = bootstrap_percentile(fem_pro, 'Swim', 1000, 75)

left = np.percentile(fem_pro_p, 2.5)
right = np.percentile(fem_pro_p, 97.5)
print(f'Bootstrap Confidence Interval for Population 75th Percentile (minutes): [{round(left/60, 2)}, {round(right/60,2)}]')

fig, ax = plt.subplots(1, figsize=(12,4))

ax.hist(fem_pro_p, bins=50, density=True, color='r', alpha=0.6)
ax.set_title('Bootstrap Sample FPRO Swim 75 Percentiles', fontsize=20)
ax.set_xlabel('Swim in Seconds', fontsize=15)

male_pro = df[df['Division'] == 'MPRO']
bootstrap_mpro_swim = bootstrap_statistic(male_pro, 'Swim', 1000, np.median)

fig, ax = plt.subplots(1, figsize=(12,7))

ax.hist(bootstrap_mpro_swim, bins=25, density=True, color='blue', alpha=0.8, label='Sample Swim Time Medians')
ax.hist(times(male_pro, 'Swim'), bins=25, density=True, color="blue", alpha=0.5, label="Sample Swims")
ax.set_title('Bootstrap Sample MPRO Swim Medians (1,000 Samples)', fontsize=20)
ax.legend()
ax.set_xlabel('Swim in Seconds', fontsize=15)

male_pro_p = bootstrap_percentile(male_pro, 'Swim', 1000, 75)

left = np.percentile(male_pro_p, 2.5)
right = np.percentile(male_pro_p, 97.5)
# 95 % Confident that this is our 75th Percentile
print(f'Bootstrap Confidence Interval for Population 75th Percentile (minutes): [{round(left/60, 2)}, {round(right/60,2)}]')

fig, ax = plt.subplots(1, figsize=(12,4))

ax.hist(male_pro_p, bins=50, density=True, color='b', alpha=0.6)
ax.set_title('Bootstrap Sample MPRO Swim 75 Percentiles', fontsize=20)
ax.set_xlabel('Swim in Seconds', fontsize=15)