**********************************************
# Ironman Kona 2019
**********************************************

#### Author: Chelsea Zaloumis
#### Galvanize DSI Capstone 1
*Last update: 7/20/2020*

![title](images/WCFinish-r.jpeg)

# Background & Motivation

The triathlon is arguably one of the most extreme and mentally taxing endurance sport competitions. Athletes train for years to complete the one-day competition consisting of a 2.4-mile (3.86 km) swim, a 112-mile (180.25 km) bicycle ride and a marathon 26.22-mile (42.20 km) run, raced in that order. Because a traithlon has three separate endurance sports, it begs the question, what comprises a strong Ironman athlete?

Every year since 1978, the World's craziest endurance athletes compete in the Kona Ironman World Championship (2020 being a COVID-exception). My goal is to explore the 2019 Ironman World Championship Results to determine which up and coming athletes sponsors should target and whether athletes with specific strengths are more likely to perform well in an Ironman triathlon.

# Data

Kaggle has a dataset that includes the 2019 Ironman World Championship Results by athlete and includes the country they are representing, their category (Professional or Age Group), their overall placing, finish time, and swim / T1 / bike / T2 / run splits. 

All of the time categories and rankings were in string format which is not helpful. My first goal was formatting the event times to actual times. The time columns began in a string format of 'datetime' and I convert them to minutes. I then cast the rank columns to integers.

| BIB | Name | Country | Gender | Division | Swim | Bike | Run | Overall | Division Rank | Gender Rank | Overall Rank | T1 | T2 |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | 
| int | string | string | string | string | string | string | string | string | string | string | string | string | string | 

I continued cleaning my data by eliminating athletes who did not finish race events and were therefore disqualified.


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
            '''
            self.df[self.col1] = self.df[self.col1].apply(lambda x: x.total_seconds())
    
        def _minutes(self):
            '''
            Converts df column from seconds to minutes
            '''
            self.df[self.col1] = self.df[self.col1].divide(60)

Resulting cleaned data:

| Name | Country | Gender | Division | Swim | Bike | Run | Overall | Division Rank | Gender Rank | Overall Rank | T1 | T2 |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | 
| object | object | object | object | float64 | float64 | float64 | float64 | int64 | int64 | int64 | float64 | float64 | 


# Exploratory Data Analysis

My first question was, do athletes have significantly different event split times based on their gender? Below are scatter plots for pro athletes on the left, and all amateurs on the right, by event type.

<img src="images/image1.png" alt="raw" width=50% height=50%/><img src="images/image1_.png" alt="raw" width=50% height=50%/>
<br>

<img src="images/image2.png" alt="raw" width=50% height=50%/><img src="images/image2_.png" alt="raw" width=50% height=50%/>
<br>

<img src="images/image3.png" alt="raw" width=50% height=50%/><img src="images/image3_.png" alt="raw" width=50% height=50%/>
<br>

<img src="images/image4.png" alt="raw" width=50% height=50%/><img src="images/image4_.png" alt="raw" width=50% height=50%/>
<br>

On average, do men race faster than women? Eyeing the scatter plots above, it would certainly seem so. To be certain, I conducted a two-sample, unpaired t-test on the pros and amateurs. My t-test states a null and alternative hypothesis as follows:

Null hypothesis: men and women mean racetimes are the same.

Alternative hypothesis: men and women mean racetimes are different, meaning one gender races faster than the other.

    t_statistic, pvalue = ttest_ind(male_pro['Overall'], fem_pro['Overall'], equal_var=False)

Pro t-test statistic: -7.76, Pro p-value: 5.156855215220441e-10

The large, negative t-test statistic value (-7.76) means there is a very big difference between the gender's mean overall times. The very small p-value allows us to reject the null hypothesis in favor of the alternative hypothesis. Therefore we can reason that pro male triathletes, on average, race faster than pro women triathletes. We can run a similar test on the amateur gender groups:

    t_statistic, pvalue = ttest_ind(male_agegroups['Overall'], fem_agegroups['Overall'], equal_var=False)

Amateur t-test statistic: -13.63, Amateur p-value: 3.889330523969423e-39

The amateur race times give us stronger reason to reject the null hypothesis and state that on average, male amateur triathletes compete faster than female amateur triathletes.

Next I plotted correlation heatmaps using the seaborn package to see what correlation split times have with division ranking. Again, we have the pro division on the left, and amateurs on the right.

<img src="images/heatmap2.png" alt="raw" width=50% height=50%/><img src="images/heatmap1.png" alt="raw" width=50% height=50%/>
<br>

T2 and run times have the greatest correlations of all the events with how pros rank. This is important to note: pro athletes need to practice their transition from bike to running as well as perform their best in running to rank higher. 

In the amateur heatmap, we can see swim has the same correlation with division rank as in the pro's heatmap. This low correlation leads us to assume that swim times do not have a big affect on how an athlete ranks. Therefore they should practice the other sports and transitions if they want to rank higher, not swimming since it so lowly correlates with division rank. However both transitions for amateurs are very important to practice as they hold the same correlation as the run event with rank.

Both heatmaps include a Bool_Gender column where female athletes result in True and male in False. The negative correlation we see in both heatmaps supports evidence from the previous scatter plots and t-tests that female athletes race slower and rank lower than male athletes, on average.

# Up & Coming Athletes

Of the amateurs, who's racing as fast as the pros and which amateur athletes should sponsors sign? To answer this, I bootstrapped the 90th percentile of pros in both genders and used a 95% confidence interval to determine the "slower" pros in event times.

        
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
        '''
        Returns an array of bootstrapped percentiles

        Parameters:
        df: dataFrame pulling from
        sport: string: 'Swim', 'Bike', 'Run', or 'Overall'
        samples: int: # of samples desired
        statistic: np.percentile
        '''
        statistics = []
        for i in range(samples):
            samp = times(df, sport)
            statistics.append(statistic(samp, percent))
        return statistics


![proswim90thpercentile](images/proswim90th.png)

![probike90thpercentile](images/probike90th.png)

![prorun90thpercentile](images/prorun90th.png)

![prooverall90thpercentile](images/prooverall90th.png)


| Event | Gender | 95% CI on 90th Percentile (min) |
| ---- | ---- | :----: |
| Swim | Female | [62.75, 75.4] |
| Swim | Male | [52.38, 57.83] |
| Bike | Female | [310.11, 333.25] |
| Bike | Male | [273.95, 283.17] |
| Run | Female | [211.39, 297.6] |
| Run | Male | [193.28, 221.37] |
| Overall | Female | [585.6, 688.37] |
| Overall | Male | [521.32, 548.9] |


The following code plots the amateur event times with the pro 95% confidence interval for their 90th percentile so we can look at what amateurs are racing like the slower pros.

    def plot_amateur_proci(sport, df1=fem_agegroups, df2=male_agegroups, df3=fem_pro, df4=male_pro):
        # Convert Amateur times to minutes
        f_agegroups_ = df1[sport] / 60
        m_agegroups_ = df2[sport] / 60

        # Generate pro bootstrap 90th percentiles
        fem_90p = bootstrap_percentile(df3, sport, 1000, 90)
        male_90p = bootstrap_percentile(df4, sport, 1000, 90)

        # Say it with confidence
        left_f90p = np.percentile(fem_90p, 2.5) / 60
        right_f90p = np.percentile(fem_90p, 97.5) / 60

        left_m90p = np.percentile(male_90p, 2.5) / 60
        right_m90p = np.percentile(male_90p, 97.5) /60

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

        m_ = m_agegroups_[m_agegroups_ <= right_m90p]
        f_ = f_agegroups_[f_agegroups_ <= right_f90p]
        mam_pros_ = round((len(m_) / len(m_agegroups_))*100, 2)
        fam_pros_ = round((len(f_) / len(f_agegroups_))*100, 2)
        print(f'Percent of male amateurs who {sport} like pros: {mam_pros_}%')
        print(f'Percent of female amateurs who {sport} like pros: {fam_pros_}%')

        return fig, ax

![amateuroverallpro90th](images/amateursoverallpro90th.png)

To save space, we'll only look at the percentages of amateurs who race like pros for the rest of the events.

| Event | Gender | % Racing like Pros |
| ---- | ---- | ---- |
| Swim | Female | 48.52% |
| Swim | Male | 8.28% |
| Bike | Female | 11.69% |
| Bike | Male | 1.74% |
| Run | Female | 72.43% |
| Run | Male | 37.09% |
| Overall | Female | 36.47% |
| Overall | Male | 2.74% |


Now we'll look at the top performing (10th percentile) amateurs and map them next to the pros 90th percentiles (with 95% confidence of course!).

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
        ax.set_xlabel(f'{sport} Time (seconds)', fontsize=15)

        return fig, ax

![amateurswim10thpro90th](images/amateur10thswimpro90th.png)

![amateurswim10thpro90th](images/amateur10thbikepro90th.png)

![amateurswim10thpro90th](images/amateur10thrunpro90th.png)

![amateurswim10thpro90th](images/amateur10thoverallpro90th.png)

The top agegroupers (amateurs) are listed here by gender. After researching, I found many of these athletes were top competitors and pro at one point, or hold agegroup championships already!

<img src="images/sponsorthesewomen.png" alt="raw" width=30% height=30%/><img src="images/sponsorthesemen.png" alt="raw" width=30% height=30%/>
<br>

# What type of athlete performs well in an Ironman Triathlon?

To answer this question, I standardized each event time (swim, bike, run) to compare how many standard deviations each athlete's time is from that category's mean time. Using the consistency function below, I defined a "consistency factor" to illustrate how consistently well, or poorly, athletes' event times are. The plot below illustrates consistency and how athletes ranked.

    def consistency(row):
        '''
        Returns difference from standardized mean
        '''
        return max(row.Norm_Swim, row.Norm_Run, row.Norm_Bike) - min(row.Norm_Swim, row.Norm_Run, row.Norm_Bike)

![consistency](images/consistency.png)

We can look at each division's consistency as well to see what agegroup holds the "all-around" athletes.

![divconsistency](images/divisionconsistency.png)

Male Pros and Males 30-39 perform the most consistently well in their respective divisions, and overall. This supports previous knowledge (not explored in this study) claiming that 30-39 is the prime age for triathletes because of how long it takes to train your body to compete in long endurance races.

Next I looked at how specialized an athlete is in a given event by defining their event specializations as the difference of the event in question from the mean of the other two events. I then plotted the pro's specializations and their rank to give us a better idea on which events the pros focus on to become the best.

![dfexample](images/stand_spec_df_ex.png)

![femprospec](images/femprospecialize.png)

![maleprospec](images/maleprospecialize.png)

Based off the above plots, we can confirm our original correlation matrix findings that show swim does not correlate with ranking and therefore should not be a focus in training. Running and biking are more so correlated with athlete rank. Male pros are incredibly specialized bikers and less so runners. Female pros specialize in running over biking. Specializing in both running and biking lead to a higher rank because of the events' percentages of overall time.

I reaffirmed these conclusions by plotting specialization by rank for each gender's division:

<img src="images/femagegroupspecialization.png" alt="raw" width=50% height=50%/><img src="images/maleagegroupspecialization.png" alt="raw" width=50% height=50%/>
<br>

## References
Dataset: https://www.kaggle.com/andyesi/2019-ironman-world-championship-results
