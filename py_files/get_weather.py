import pandas as pd
import datetime
import numpy as np
from scipy import stats

import seaborn as sns
sns.set_style('whitegrid')
import matplotlib.pyplot as plt


def get_weather():
    df = pd.read_csv("merge_2.csv")
    df.drop('Unnamed: 0', axis=1, inplace = True)

    #create a new dataframe with score and weather_binary, 1 = precipitation, 0 = no precipitation
    weather_score = df[['SCORE', 'weather_binary']]
    #seperate scores on precipitation days and no precipitation days into numpy arrays
    precip = np.array(weather_score['SCORE'][weather_score['weather_binary']==1])
    no_precip = np.array(weather_score['SCORE'][weather_score['weather_binary']==0])

    print("The mean score on days with precipitation is ", round(precip.mean(), 2))
    print("With a standard deviation of ", round(precip.std(), 3))

    print("The mean score on days without precipitation is ", round(no_precip.mean(), 2))
    print("With a standard deviation of ", round(no_precip.std(), 3))

    sns.set(color_codes=True)
    plt.figure(figsize=(12, 8))
    sns.distplot(precip, bins=20) #blue line
    sns.distplot(no_precip, bins=20); #orange line

    t_stat_weather, p_value_weather = stats.ttest_ind(precip, no_precip, equal_var=False)
    print("The t-stat is {} and the the p value is {}.".format(round(t_stat_weather, 3), round(p_value_weather, 3)))

    #calculating critical value
    deg_weather = len(precip) + len(no_precip) - 2
    t_critical_weather = np.round(stats.t.ppf(1 - 0.05, df=deg_weather),4)
    t_critical_weather

    xs = np.linspace(-5, 5, 200)
    ys = stats.t.pdf(xs, deg_weather, 0, 1)

    fig = plt.figure(figsize=(12,8))

    ax = fig.gca()

    ax.plot(xs, ys, linewidth=3, color='darkblue')

    ax.axvline(t_stat_weather, color='red', linestyle='--', lw=3,label='t-stat')

    ax.axvline(t_critical_weather,color='green',linestyle='--',lw=3,label='critical t-value')

    ax.fill_betweenx(ys,xs,t_critical_weather,where = xs > t_critical_weather, color = 'blue')

    ax.legend()
    plt.show()

    print("The critical value of {} is larger than the t-statistic of {}, with a p-value of {}. Therefore we fail to reject the null hypothesis.".format(t_critical_weather, round(t_stat_weather, 3), round(p_value_weather,3)))

