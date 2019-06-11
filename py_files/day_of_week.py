import pandas as pd
import datetime
import numpy as np
from scipy import stats

import seaborn as sns
sns.set_style('whitegrid')
import matplotlib.pyplot as plt

def day_of_week():
    
    df = pd.read_csv("csv/merge_2.csv")
    df.drop('Unnamed: 0', axis=1, inplace = True)

    #create new data frame with score and day of the week
    days_df = df[['SCORE','DAY OF WEEK']]
    #seperate out and create 2 more data frames. One for Monday/Tuesday, one for Thursday/Friday
    mon = days_df[days_df['DAY OF WEEK'] == 'Monday']
    tues = days_df[days_df['DAY OF WEEK'] == 'Tuesday']
    thurs = days_df[days_df['DAY OF WEEK'] == 'Thursday']
    fri = days_df[days_df['DAY OF WEEK'] == 'Friday']

    mon_tues = pd.concat([mon, tues])
    thurs_fri = pd.concat([thurs, fri])

    #turn the scores in each data frame into a numpy array 
    montue = np.array(mon_tues['SCORE'])
    thurfri = np.array(thurs_fri['SCORE'])

    print("The mean inspection score for Monday's and Tuesday's is ", round(montue.mean(), 3))
    print("With a standard deviation of ", round(montue.std(), 3))

    print("The mean inspection score for Thursday's and Friday's is ", round(thurfri.mean(), 3))
    print("With a standard deviation of ", round(thurfri.std(), 3))

    t_stat_week, p_value_week = stats.ttest_ind(montue, thurfri, equal_var=False)
    print("The t-stat is {} and the the p value is {}.".format(round(t_stat_week, 3), round(p_value_week, 4)))  

    #calculating critical value
    deg_week = len(montue) + len(thurfri) - 2
    t_critical_week = np.round(stats.t.ppf(1 - 0.05, df=deg_week),4)
    t_critical_week

    xs = np.linspace(-5, 5, 200)
    ys = stats.t.pdf(xs, deg_week, 0, 1)

    fig = plt.figure(figsize=(12,8))

    ax = fig.gca()

    ax.plot(xs, ys, linewidth=3, color='darkblue')

    ax.axvline(t_stat_week, color='red', linestyle='--', lw=3,label='t-stat')

    ax.axvline(t_critical_week,color='green',linestyle='--',lw=3,label='critical t-value')

    ax.fill_betweenx(ys,xs,t_critical_week,where = xs > t_critical_week, color = 'blue')

    ax.legend()
    plt.show()

    print("The critical value of {} is less than the t-statistic of {}, with a p-value of {}. Therefore we are able to reject the null hypothesis.".format(t_critical_week, t_stat_week, p_value_week ))
