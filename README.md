**********************************************
# Ironman Kona 2019
**********************************************

#### Author: Chelsea Zaloumis
#### Galvanize DSI Capstone 1
*Last update: 7/20/2020*

![title](images/WCFinish-r.jpeg)

# Background & Motivation

The triathlon is arguably one of the most extreme and mentally taxing endurance sport competitions. Athletes train for years to complete the one-day competition consisting of a 2.4-mile (3.86 km) swim, a 112-mile (180.25 km) bicycle ride and a marathon 26.22-mile (42.20 km) run, raced in that order. Because a traithlon has three separate endurance sports, it begs the question, what comprises a strong Ironman athlete?

Every year since 1978, the World's craziest endurance athletes compete in the Kona Ironman World Championship (2020 being a COVID-exception). My goal is to explore the 2019 Ironman World Championship Results to determine if athletes hailing from specific backgrounds are more likely to perform well in an Ironman triathlon.

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

![proheat](images/heatmap1.png) ![amateurheat](images/heatmap2_.png)

Swim times have a much lower correlation in the pro division where bike and run times are highly correlated with overall finish times. This has to do with the total distance of the event, 226.31km, and how that's divided amongst the three sports. Swim accounts for 1.7% of the entire race, bike 79.6%, and run is 18.7%. Meaning bike and run times dominate the overall time.

Even more interesting is the correlation amongst event times and division rank: T2 and run times have the greatest correlations of all the events with how pros rank. This is important to note: pro athletes need to practice their transition from bike to run and need to perform best in running to rank higher. 

In the amateur heatmap, we can see swim has the lowest correlation with ranking than the other event times. However both transitions for amateurs are very important to practice as they hold the same correlation as the run event with rank.

Both heatmaps include a Bool_Gender column where female athletes result in True and male in False. the negative correlation we see in both heatmaps supports evidence from the previous scatter plots and t-tests that female athletes race slower and rank lower than male athletes, on average.


## References
Dataset: https://www.kaggle.com/andyesi/2019-ironman-world-championship-results


- - -
* notes *
-who is interested in this data?
-sponsors for up and coming athletes? sponsoring high ranking amateurs => more exposure and approachability
