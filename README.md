# Analysis of Weather Data using SQLite and Flask

## Overview
This analysis delves into a SQLite database containing weather data from the Hawaiian island of Oahu. This dataset contains temperature and precipitation (rain) recordings taken across several weather stations in Oahu. The intent here is to support a business case to validate whether it would be a good idea to establish a surf and ice cream shop (reliant on sunlight and warm temperatures) on Oahu.

**Technologies used:**
- Python 3.7.9
- SQLite
- SQLAlchemy
- Flask
- Pandas & NumPy

## Results

- The average temperature in June (Summer Solstice) across several years of data in our dataset was 74.9F (or 23.8 degrees Celsius). Compared to the average temperature in December (Winter Solstice) 71F (or 21.6 degrees Celsius), we can conclude that there is only a **2 degrees Celsius difference between the 'warmest' and 'coldest' months of the year in Oahu.**

- The minimum temperature detected in June was 64F (17.7 degrees Celsius), while the minimum in December was 56F (13 degrees Celsius). This means that there may be certain days where a surf and ice cream shop may not enjoy peak business, as the cold weather may deter surfers from surfing, let alone buying ice cream that day.

- The Coefficient of Variance for June temperatures was: `3.25/74.94 = 0.043`
- The Coefficient of Variance for December temperatures was: `3.75/71.04 = 0.052`
- With such a similar Coefficient of Variance for both months, we can assume that **the weather in both months will be generally very similar.**

## Summary & Exploration

One possible question is "What is the proportion of days that had absolutely zero precipitation", otherwise considered "clear days"? We can query our dataset with the following query:

`zero_precipitation_proportion = (session.query(Measurement.prcp).filter(Measurement.prcp == '0').count()/session.query(Measurement.prcp).count())`


Another question we could ask is the average temperature detected in each month

**Query**

`
avg_temps = session.query(extract('month',Measurement.date),
            func.avg(Measurement.tobs)).\
    group_by(extract('month',Measurement.date)).all()`

**Dataframe & cleaning**

`
avg_temps_df = pd.DataFrame(avg_temps,columns=["Month","avg_temp (F)"])
avg_temps_df.set_index(avg_temps_df['Month'], inplace=True)
avg_temps_df.index = month_list
avg_temps_df.drop(["Month"],axis=1)`

**Output**

![avg_temp_df](/assets/avg_temp_df.png)

As we can see, in terms of real world feel, there is very little variance between the average temperatures. The variance is close to 8F which is ~4 degrees Celsius. 