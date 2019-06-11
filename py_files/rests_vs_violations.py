import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress


def rests_vs_violations():

        # ------------------------------------------------------------------------------------
        # the unique_inspection.csv file was created o get one row for each inspection using
        # a restaurants "CAMIS" identifier and inspection date. It is not combined with other
        # data. We create a new DataFrame which contains unique names and a count of those
        # names (df_ex). We eventually get the restaurant name, inspection mean, and count
        # of how many restaurants with that name are in the records.
        # ------------------------------------------------------------------------------------

    def get_info():
        df = pd.read_csv('csv/unique_inspection.csv')
        df_names = pd.DataFrame(
            {'DBA': df['DBA'],
             'CAMIS': df['CAMIS'],
            })
        df_names.drop_duplicates(subset=['CAMIS'], keep = 'first', inplace = True)
        df_name_count = df_names.groupby(['DBA']).count().sort_values(['CAMIS'], ascending=False)
        df_name_count.reset_index(inplace = True)
        df_name_count.rename(columns = {'CAMIS': 'restaurants'}, inplace = True)
        df_ex = pd.merge(df, df_name_count, how='left', on='DBA')
        df_score = df_ex.groupby(['restaurants']).sum().sort_values(['SCORE'], ascending=False)
        df_count = df_ex.groupby(['restaurants']).count().sort_values(['SCORE'], ascending=False)
        df_count = df_count.reset_index(inplace = False)
        df_count = df_count[['restaurants', 'Unnamed: 0']]
        df_count.rename(columns = {'Unnamed: 0' : 'count'}, inplace = True)
        df_score_count = pd.merge(df_count, df_score, how='left', on='restaurants')
        df_score_count['meany'] = df_score_count['SCORE'] / df_score_count['count']

        # ------------------------------------------------------------------------------------
        # Creates a plot that compares the mean inspection scores based on the number of
        # restaurants with that name that exists in the city.
        # ------------------------------------------------------------------------------------

        area = np.pi*10
        y = df_score_count.meany
        x = df_score_count.restaurants

        plt.figure(figsize=(12, 8))
        plt.scatter(x, y, s=area, alpha=1)
        plt.title('Mean Inspection Score')
        plt.xlabel('Restaurants')
        plt.ylabel('Mean Score')

        plt.axhline(df_ex['SCORE'].mean(), color='b')
        
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        plt.plot(x,p(x),"r--")

        plt.legend(('NYC Mean Score', 'Restaurant Locations vs Score Trendline', 'Mean Score per Restaurant Locations'))


        # ------------------------------------------------------------------------------------
        # Linear regression of what is charted above.
        # ------------------------------------------------------------------------------------

        print('Linear Regression Restaurant Count vs Restaurant Score:')
        print(linregress(df_score_count['meany'], df_score_count['restaurants']))

        # ------------------------------------------------------------------------------------
        # Pret A Manger's score is abnormally low across the board. It is possible that 
        # because it is not a franchise, the rules are closely followed and as a result 
        # it does not see a lot of unclean kitchens. The next few steps removes it from
        # consideration.
        # ------------------------------------------------------------------------------------

        minus_pret = df_score_count[df_score_count['meany'] > 7.4]

        # --------------------------------------
        # see above
        # --------------------------------------

        area = np.pi*10
        y = minus_pret.meany
        x = minus_pret.restaurants

        plt.figure(figsize=(12, 8))
        plt.scatter(x, y, s=area, alpha=1)
        plt.title('Mean Inspection Score, Without Pret A Manger')
        plt.xlabel('Restaurants')
        plt.ylabel('Mean Score')

        plt.axhline(df_ex['SCORE'].mean(), color='b')
        
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        plt.plot(x,p(x),"r--")

        plt.legend(('NYC Mean Score', 'Restaurant Locations vs Score Trendline', 'Mean Score per Restaurant Locations'))

        plt.show()
        
        print('Linear Regression Restaurant Count vs Restaurant Score without Pret A Manger:')

        print(linregress(minus_pret['restaurants'], minus_pret['meany']))

    get_info()
