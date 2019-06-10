# The Data:

Sources:
- **DOHMH New York City Restaurant Inspection Results**
    - From 2017-06-01 through 2019-06-05
    - 268,458 health code violations
    - 84,576 inspections
    - 20,697 retaurants
    - https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/43nn-pn8j
- **Dark Sky API**
    - Weather data for the 641 dates where inspections occured during those two years
    - https://darksky.net/dev
- **311 Service Requests from 2010 to Present**
    - Used API to receive 254,171 rodent-related complaints
    - https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9
    - https://dev.socrata.com/foundry/data.cityofnewyork.us/fhrw-4uyv
    
## Hypothesis 1: The more locations of a restaurant, the lower the code violation score

## Result of testing Hypothesis 1
The p-value **with** Pret A Manger, which seems like an outlier, is 0.016. With it removed from the dataset, the p-value is 0.010. Both are below 0.05, which would allow us to reject the null hypothesis.

![alt text](mean-inspection-score)

    
