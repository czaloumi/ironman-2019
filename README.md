**********************************************
# Kona Ironman 2019
**********************************************

#### Author: Chelsea Zaloumis
#### Galvanize DSI Capstone 1
*Last update: 12/28/2020*

![title](images/WCFinish-r.jpeg)

# Background & Motivation

The triathlon is arguably one of the most extreme and mentally taxing endurance sport competitions. Athletes train for years to complete the one-day competition consisting of a 2.4-mile (3.86 km) swim, a 112-mile (180.25 km) bicycle ride and a marathon 26.22-mile (42.20 km) run, raced in that order. Because a traithlon has three separate endurance sports, it begs the question, what comprises a strong Ironman athlete?

Every year since 1978, the World's top (craziest) endurance athletes compete in the Kona Ironman World Championship (2020 being a COVID-exception). My goal is to explore the 2019 Ironman World Championship Results to determine which up and coming athletes sponsors should target and whether athletes with specific strengths are more likely to perform well in an Ironman triathlon.

# Data

I used a Kaggle dataset of the 2019 Ironman World Championship Results, which is linked in references. Rows are entries by athlete and include the country they are representing, their category (Professional or Age Group), their overall placing, finish time, and swim / T1 / bike / T2 / run splits. The dataset originally consisted of 14 columns and 3,045 rows or athletes.

All of the time categories and rankings were in string format. I formatted the event times to a float: i.e. converted string format of 'datetime' to minutes. I then cast the rank columns to integers. I continued cleaning my data by eliminating athletes who did not finish race events and were therefore disqualified as well as the BIB column. Resulting cleaned data and datatypes:

| Name | Country | Gender | Division | Swim | Bike | Run | Overall | Division Rank | Gender Rank | Overall Rank | T1 | T2 |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | 
| object | object | object | object | float64 | float64 | float64 | float64 | int64 | int64 | int64 | float64 | float64 | 


# Battle of the Sexes
A debate as old as time... do ironman athletes have significantly different event times based on their gender? Below are scatter plots of event times for pro athletes and amateurs by gender.

<img src="images/pro-29-Dec-2020.png"/>
<br>

<img src="images/amateur-29-Dec-2020.png"/>

On average, do men race faster than women? Eyeing the scatter plots above, it would certainly seem so. Generating bootstrapped samples from the professional race times and plotting the difference in their averages, we can visualize the mean difference in professional gender race time below.

<img src="images/mpro-fpro-13-Jan-2021.png" width=80% height=80%/>

The histograms do not contain 0 so we can conclude that there is a statistically significant difference in pro triathlon times based on gender. I conducted a two-sample, unpaired t-test on the pros and amateurs. My t-test states a null and alternative hypothesis as follows:

* Null hypothesis: men and women mean racetimes are the same.

* Alternative hypothesis: men and women mean racetimes are different, meaning one gender races faster than the other.

        Pro t-test statistic: -7.76, Pro p-value: 0.0

The significant p-value allows us to reject the null hypothesis in favor of the alternative hypothesis. Therefore we can reason that **pro male triathletes, on average, race faster than pro female triathletes.**

We can run a similar test on the amateur gender groups:

        Amateur t-test statistic: 0.45, Amateur p-value: 0.65

The amateur race times yield a less significant p-value therefore we cannot reject the null hypothesis. **Amateur male and female triathletes have similar racetimes, on average.**

It's important to note that by "amateur" we are referring to anyone who is not in the professional division. This bucket is sensitive to outliers.

The following correlation heatmaps allow us to view correlations between event times and athlete division ranking.

<img src="images/proheatmap.png" alt="raw" width=50% height=50%/><img src="images/amateurheatmap.png" alt="raw" width=50% height=50%/>
<br>

  * T2 and run times have the greatest correlations of all the events with professional division rank.
        * Therefore pro athletes need to practice their transition from bike to running as well as perform their best in running to rank higher. 


  * Swim has the lowest correlation than the other events, therefore swim times do not have as big affect on how an athlete ranks. 
  * Both transitions for amateurs are very important to practice as they hold the same correlation as the run event with rank.


  * The negative correlation in both heatmaps' Gender columns supports evidence from the previous scatter plots and t-tests that female athletes race slower and rank lower than male athletes, on average.

# Up & Coming Athletes

Of the amateurs, who's racing as fast as the pros and therefore which amateur athletes should sponsors focus on? To answer this, I bootstrapped the 90th percentile of professionals in both genders and used a 95% confidence interval to determine the "slow" pros. Similarly, I bootstrapped the 10th percentile amateurs to only plot the "fast" amateurs.


| Event | Gender | 95% CI on 90th Percentile (min) | % Amateurs in 95% CI |
| ---- | ---- | :----: | :----: |
| Swim | Female | [63.83, 75.4] | 48.52% |
| Swim | Male | [52.42, 57.83] | 8.28% |
| Bike | Female | [310.57, 331.46] | 11.69% |
| Bike | Male | [273.95, 283.17] | 1.74% |
| Run | Female | [213.72, 297.6] | 72.43% |
| Run | Male | [193.7, 216.03] | 37.09% |
| Overall | Female | [586.72, 688.37] | 36.47% |
| Overall | Male | [524.48, 545.48] | 2.74% |


I visualized this data with the following plots of bootstrapped top performing (10th percentile) amateurs with the pro's 90th percentiles (with 95% confidence of course).

![amateurswim10thpro90th](images/swim_comparison.png)

![amateurswim10thpro90th](images/bike_comparison.png)

![amateurswim10thpro90th](images/run_comparison.png)

![amateurswim10thpro90th](images/overall_comparison.png)

And just who are these fast amateurs? After researching the lists below, I found that most were previously professional athletes.

<img src="images/top_10f_amateurs.png" alt="raw"/><img src="images/top_10m_amateurs.png" alt="raw"/>
<br>

# What type of athlete performs well in an Ironman Triathlon?

To answer this question, I standardized each event time (swim, bike, run) to compare how many standard deviations each athlete's time is from that category's mean time. Displayed below is each athlete's "consistency factor" to illustrate how consistently well, or poorly, athletes' event times are.

![consistency](images/consistency.png)

Not surprisingly, the more consistently fast their event times, the higher ranking an athlete.

We can look at each division's consistency as well to see what agegroup holds the "all-around" athletes.


![divconsistency](images/divisionconsistency.png)

Eyeing this plot, male pros and males 30-39 perform the most consistently well in their respective divisions and overall. This supports previous knowledge (not explored in this study) claiming that 30-39 is the prime age for triathletes on account of how long it takes to train your body to compete in endurance races.

Next I looked at how specialized an athlete is in a given event by defining their event specializations.  An event's specialization is equal to difference of the event in question from the mean of the other two events. The plots below allow us to visualize how specialized the pro traithletes are by gender.

![prospec](images/pro_specialize.png)

Observations:
  * Swim has a dispersed specialization amongst the pros.
  * Male pros are incredibly specialized bikers and less so runners.
  * Female pros specialize in running over biking.
  * Specializing in both running and biking lead to a higher rank because of the events' percentages of overall time.
  
The following results are for a two-sample, unpaired t-test with a null and alternative hypothesis as follows:

* **Null hypothesis**: Athletes who specialize in a certain event race just as fast as the athletes who do not specialize.

* **Alternative hypothesis**: Athletes who specialize in a certain event have overall competition times that are greater, or smaller than the mean of overall times of athletes who do not specialize.

| Event | P-value | T-test Statistic |
| ---- | ---- | :----: |
| Swim | 0.0 | 7.5 |
| Bike | 0.0 | -6.69 |
| Run | 0.0 | -3.32 |

The significant p-values indicate we reject the null hypothesis and accept our alternative hypothesis that athletes who specialize in at least one sport have overall race times that are greater or less than the non-specializing athlete's overall mean times. Swim specializing athletes have greater overall times than the non-specializing swim athlete overall race time average. Bike and run specializing athletes finish with an overall time that is faster than the mean overall time of their non-specializing competitors.

# Future Direction

With more time, I'd like to add to my overall data with results from Kona's 16-18 championships and find data on athlete training regiments and physiological tests to explore who was built for triathlon, and if you can train to overcome physiological impediments.

## References
Dataset: https://www.kaggle.com/andyesi/2019-ironman-world-championship-results
