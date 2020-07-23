**********************************************
# Ironman Kona 2019
**********************************************

#### Author: Chelsea Zaloumis
#### Galvanize DSI Capstone 1
*Last update: 7/20/2020*

![title](images/WCFinish-r.jpeg)

# Background & Motivation

The triathlon is arguably one of the most extreme and mentally taxing endurance sport competitions. Athletes train for years to complete the one-day competition consisting of a 2.4-mile (3.86 km) swim, a 112-mile (180.25 km) bicycle ride and a marathon 26.22-mile (42.20 km) run, raced in that order. Because a traithlon has three separate endurance sports, it begs the question, what comprises a strong Ironman athlete?

Every year since 1978, the World's craziest endurance athletes compete in the Kona Ironman World Championship (2020 being a COVID-exception). My goal is to explore the 2019 Ironman World Championship Results to determine which up and coming athletes sponsors should target and whether athletes hailing from specific backgrounds are more likely to perform well in an Ironman triathlon.

# Data

Kaggle has a dataset that includes the 2019 Ironman World Championship Results by athlete and includes the country they are representing, their category (Professional or Age Group), their overall placing, finish time, and swim / T1 / bike / T2 / run splits. 

# Exploratory Data Analysis

After importing my data using Spark, I quickly converted my data to pandas and using timecleaning.py, converted all timedate data types into minutes. I continued cleaning my data by eliminating athletes who did not finish race events and were therefore disqualified.


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


My first question was, do pro athletes have significantly different event split times based on their gender? Below are scatter plots for pro athletes on the left, and all amateurs on the right, by event type.

![proswim](images/image1.png) ![amateurswim](images/image1_.png)

![probike](images/image2.png) ![amateurbike](images/image2_.png)

![prorun](images/image3.png) ![amateurbike](images/image3_.png)

![prooverall](images/image4.png) ![amateuroverall](images/image4_.png)

On average, do men race faster than women? Eyeing the scatter plots above, it would certainly seem so. To be certain, I conducted a two-sample, unpaired t-test on the pros and amateurs. My t-test states a null and alternative hypothesis as follows:

Null hypothesis: men and women mean racetimes are the same.

Alternative hypothesis: men and women mean racetimes are different, meaning one gender races faster than the other.

    t_statistic, pvalue = ttest_ind(male_pro['Overall'], fem_pro['Overall'], equal_var=False)

Pro t-test statistic: -7.76, Pro p-value: 5.156855215220441e-10

The large, negative t-test statistic value (-7.76) means there is a very big difference between the gender's mean overall times. The very small p-value allows us to reject the null hypothesis in favor of the alternative hypothesis. Therefore we can reason that pro male triathletes, on average, race faster than pro women triathletes. We can run a similar test on the amateur gender groups:

    t_statistic, pvalue = ttest_ind(male_agegroups['Overall'], fem_agegroups['Overall'], equal_var=False)

Amateur t-test statistic: -13.63, Amateur p-value: 3.889330523969423e-39

The amateur race times give us stronger reason to reject the null hypothesis and state that on average, male amateur triathletes compete faster than female amateur triathletes.

Next I plot correlation heatmaps using the seaborn package to see what correlation split times have with division ranking. Again, we have the pro division on the left, and amateurs on the right.

![proheat](images/heatmap2.png) ![amateurheat](images/heatmap1.png)

T2 and run times have the greatest correlations of all the events with how pros rank. This is important to note: pro athletes need to practice their transition from bike to running to shave time off T2 as well as perform their best in running to rank higher. 

In the amateur heatmap, we can see swim has the lowest correlation with ranking than the other event times. However both transitions for amateurs are very important to practice as they hold the same correlation as the run event with rank.

Both heatmaps include a Bool_Gender column where female athletes result in True and male in False. the negative correlation we see in both heatmaps supports evidence from the previous scatter plots and t-tests that female athletes race slower and rank lower than male athletes, on average.

# Up & Coming Athletes

Of the amateurs, who's racing as fast as the pros and which amateur athletes should sponsors sign? To answer this, I bootstrapped the 90th percentile and used a 95% confidence interval to determine the "slower" pros in event times. The following code returns a random array of event times, bootstraps any statistic provided by numpy, and then plots the pro 90th percentiles and 95% confidence intervals.

    def times(df, sport):
        '''
        Returns an array of randomly chosen times according to the sport specified.
    
        Parameters:
        df: dataFrame pulling from
        sport: string: 'Swim', 'Bike', 'Run', or 'Overall'
    
        Returns:
        np.array of length 2434, with time entries in minutes
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

        ax.axvline(left_f90p, c='pink', linestyle="--")
        ax.axvline(right_f90p, c='pink', linestyle="--")
        ax.axvline(left_m90p, c='grey', linestyle="--")
        ax.axvline(right_m90p, c='grey', linestyle="--")

        print(f'Female Pro {sport} Times Bootstrap Confidence Interval for Population 90th Percentile (minutes): [{round(left_f90p, 2)}, {round(right_f90p,2)}]')
        print(f'Male Pro {sport} Times Bootstrap Confidence Interval for Population 90th Percentile (minutes): [{round(left_m90p, 2)}, {round(right_m90p,2)}]')

        return fig, ax


![proswim90thpercentile](images/proswim90th.png)

Female Pro Swim Times Bootstrap Confidence Interval for Population 90th Percentile (minutes): [62.75, 75.4]
Male Pro Swim Times Bootstrap Confidence Interval for Population 90th Percentile (minutes): [52.38, 57.83]

![probike90thpercentile](images/probike90th.png)

Female Pro Bike Times Bootstrap Confidence Interval for Population 90th Percentile (minutes): [310.11, 333.25]
Male Pro Bike Times Bootstrap Confidence Interval for Population 90th Percentile (minutes): [273.95, 283.17]

![prorun90thpercentile](images/prorun90th.png)

Female Pro Run Times Bootstrap Confidence Interval for Population 90th Percentile (minutes): [211.39, 297.6]
Male Pro Run Times Bootstrap Confidence Interval for Population 90th Percentile (minutes): [193.28, 221.37]

![prooverall90thpercentile](images/prooverall90th.png)

Female Pro Overall Times Bootstrap Confidence Interval for Population 90th Percentile (minutes): [585.6, 688.37]
Male Pro Overall Times Bootstrap Confidence Interval for Population 90th Percentile (minutes): [521.32, 548.9]


## References
Dataset: https://www.kaggle.com/andyesi/2019-ironman-world-championship-results


- - -
* notes *
-who is interested in this data?
-sponsors for up and coming athletes? sponsoring high ranking amateurs => more exposure and approachability
