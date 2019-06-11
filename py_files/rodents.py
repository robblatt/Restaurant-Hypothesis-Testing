import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols
import matplotlib.pyplot as plt
import pylab
plt.style.use('seaborn')

    
def rodents_per_violation():
    
    # ----------------------------------------------------------------------------
    # the df_rat_complaints_by_zipcode.csv comes from the 311 dataset and only
    # pulls the complaints that are directly rodent related. We combined that with
    # the violations in restaurant inspections that were specifically about
    # seeing rodents.
    # ----------------------------------------------------------------------------

    complaints_by_zipcode = pd.read_csv('df_rat_complaints_by_zipcode.csv')
    complaints_by_zipcode.drop(['Unnamed: 0'], axis = 1, inplace = True)
    complaints_by_zipcode.rename(columns={"incident_zip":"ZIPCODE"}, inplace=True)

    violations_per_zip = pd.read_csv('violations_per_zip.csv')
    df_rodents = pd.merge(violations_per_zip, complaints_by_zipcode, on='ZIPCODE')
    df_rodents['vio_per_insp'] = df_rodents.violation_count / df_rodents.inspections
    df_rodents_ols = df_rodents

    df_rodents_ols.drop(['Unnamed: 0', 'inspections', 'violation_count', 'ZIPCODE'], axis=1, inplace = True)

    # ----------------------------------------------------------------------------
    # Take a look at how they interact on a plot
    # ----------------------------------------------------------------------------

    area = np.pi*10
    y = df_rodents_ols.vio_per_insp
    x = df_rodents_ols.complaints

    plt.figure(figsize=(12, 8))
    plt.scatter(x, y, s=area, alpha=1)
    plt.title('Violations per Inspection vs. 311 Rodent Complaints')
    plt.xlabel('311 Rodent Complaints')
    plt.ylabel('Violations per Inspection')

    plt.axhline(df_rodents_ols.vio_per_insp.mean(), color='b')

    pylab.plot(x,y,'o')

    # calc the trendline
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    pylab.plot(x,p(x),"r--")

    plt.legend(('NYC Mean V/I Score', 'Violations per Inspection', 'Trendline'))

    plt.show()

    # ----------------------------------------------------------------------------
    # Now to see if we can predict the amount of rodent related violations per
    # inspection based on the number of 311 complaints received in that zipcode.
    # With more time, we would have liked to predict the likelihood of an
    # restaurants within a zipcode to have a rodent violation.
    # ----------------------------------------------------------------------------

    formula = "vio_per_insp ~ complaints"
    model = ols(formula= formula, data=df_rodents_ols).fit()
    outcome = 'vio_per_insp'
    predictors = df_rodents_ols.drop('vio_per_insp', axis=1)
    pred_sum = "+".join(predictors.columns)
    formula = outcome + "~" + pred_sum
    model = ols(formula= formula, data=df_rodents_ols).fit()
    print(model.summary())