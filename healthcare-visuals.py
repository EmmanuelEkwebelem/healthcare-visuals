import pandas
import numpy
import seaborn
import plotly.express as px
import matplotlib.pyplot as plt

seaborn.set_theme(style="whitegrid")
print('cell successfully ran')

### Loading in the data 
Data = pandas.read_csv('https://raw.githubusercontent.com/mengyao36/AHI_Microcourse_Visualization/main/Data/Georgia_COVID/Georgia_COVID-19_Case_Data.csv')
Data

### Describing the variables
len(Data)
Data.shape
Data.info()
list(Data)

Data['COUNTY'].value_counts()
Data_counties = Data['COUNTY'].value_counts()
Data_counties.head(5)

### Transforming Columns
Data['DATESTAMP']
Data['DATESTAMP_MOD'] = Data['DATESTAMP']
print(Data['DATESTAMP_MOD'].head(10))
print(Data['DATESTAMP_MOD'].dtypes)

Data['DATESTAMP_MOD'] = pandas.to_datetime(Data['DATESTAMP_MOD'])
Data['DATESTAMP_MOD'].dtypes

Data[['DATESTAMP', 'DATESTAMP_MOD']]

Data['DATESTAMP_MOD_DAY'] = Data['DATESTAMP_MOD'].dt.date
Data['DATESTAMP_MOD_DAY']

Data['DATESTAMP_MOD_YEAR'] = Data['DATESTAMP_MOD'].dt.year
Data['DATESTAMP_MOD_MONTH'] = Data['DATESTAMP_MOD'].dt.month

Data['DATESTAMP_MOD_YEAR']
Data['DATESTAMP_MOD_MONTH']

Data['DATESTAMP_MOD_MONTH_YEAR'] = Data['DATESTAMP_MOD'].dt.to_period('M')
Data['DATESTAMP_MOD_MONTH_YEAR'].sort_values()
Data

Data['DATESTAMP_MOD_WEEK'] = Data['DATESTAMP_MOD'].dt.week
Data['DATESTAMP_MOD_WEEK']

Data['DATESTAMP_MOD_QUARTER'] = Data['DATESTAMP_MOD'].dt.to_period('Q')
Data['DATESTAMP_MOD_QUARTER']

Data['DATESTAMP_MOD_QUARTER'].sort_values()

Data['DATESTAMP_MOD_DAY_STRING'] = Data['DATESTAMP_MOD_DAY'].astype(str)
Data['DATESTAMP_MOD_WEEK_STRING'] = Data['DATESTAMP_MOD_WEEK'].astype(str)
Data['DATETIME_STRING'] = Data['DATESTAMP_MOD_MONTH_YEAR'].astype(str)

### Getting the counties required for our analysis
# We know that the counties we want to analysis our: Cobb, DeKalb, Fulton, Gwinnett, Hall

Data['COUNTY']

countList = ['COBB', 'DEKALB', 'FULTON', 'GWINNETT', 'HALL']
countList

selectCounties = Data[Data['COUNTY'].isin(countList)]
len(selectCounties)

# Getting just the specific date/time frame we want
# Data = length ~90,000
# selectCounties = length 2,830
# selectCountyTime = ???/TBD

selectCountyTime = selectCounties
selectCountyTime['DATESTAMP_MOD_MONTH_YEAR']

selectCountyTime_april2020 = selectCountyTime[selectCountyTime['DATESTAMP_MOD_MONTH_YEAR'] == '2020-04']
len(selectCountyTime_april2020)

selectCountyTime_aprilmay2020 = selectCountyTime[(selectCountyTime['DATESTAMP_MOD_MONTH_YEAR'] == '2020-05') | (selectCountyTime['DATESTAMP_MOD_MONTH_YEAR'] == '2020-04')]
len(selectCountyTime_aprilmay2020)

selectCountyTime_aprilmay2020.head(50)

### NewDataFram made up of specific columns we want
NewData = selectCountyTime_aprilmay2020[['COUNTY','DATESTAMP_MOD','DATESTAMP_MOD_DAY','DATESTAMP_MOD_DAY_STRING','DATETIME_STRING','DATESTAMP_MOD_MONTH_YEAR','C_New','C_Cum','H_New','H_Cum','D_New','D_Cum']]
NewData

### Assessing Covid cases per month
NewData_dropdups = NewData.drop_duplicates(subset=['COUNTY', 'DATETIME_STRING'], keep='last')
NewData_dropdups

pandas.pivot_table(NewData_dropdups, values='C_Cum', index=['COUNTY'],columns=['DATESTAMP_MOD_MONTH_YEAR'], aggfunc=numpy.sum)

vis1 = seaborn.barplot(x='DATESTAMP_MOD_MONTH_YEAR', y='C_Cum', data=NewData_dropdups)
vis2 = seaborn.barplot(x='DATESTAMP_MOD_MONTH_YEAR', y='C_Cum', hue='COUNTY', data=NewData_dropdups)

plotlyl = px.bar(NewData_dropdups, x='DATETIME_STRING', y='C_Cum', color='COUNTY', barmode='group')
plotlyl.show()

plotlyl = px.bar(NewData_dropdups, x='DATETIME_STRING', y='C_Cum', color='COUNTY', barmode='stack')
plotlyl.show()

#### Assessing Covid cases per day 
daily = NewData
daily
len(daily)

pandas.pivot_table(daily, values='C_Cum', index=['COUNTY'], columns=['DATESTAMP_MOD_DAY'], aggfunc=numpy.sum)
pandas.pivot_table(daily, values='C_Cum', index=['DATESTAMP_MOD_DAY'], columns=['COUNTY'], aggfunc=numpy.sum)

startdate = pandas.to_datetime('2020-04-26').date()
enddate = pandas.to_datetime('2020-05-09').date()

maskFilter = (daily['DATESTAMP_MOD_DAY'] >= startdate) & (daily['DATESTAMP_MOD_DAY'] <= enddate)
dailySpecific = daily.loc[maskFilter]
dailySpecific

dailySpecific[dailySpecific['COUNTY'] == 'FULTON']

vis3 = seaborn.lineplot(data=dailySpecific, x='DATESTAMP_MOD_DAY', y='C_Cum')
vis3 = seaborn.lineplot(data=dailySpecific, x='DATESTAMP_MOD_DAY', y='C_Cum', hue='COUNTY')

plotly3 = px.bar(dailySpecific, x='DATESTAMP_MOD_DAY', y='C_Cum', color='COUNTY')
plotly3.show()

plotly4 = px.bar(dailySpecific, x='DATESTAMP_MOD_DAY', y='H_New', color='COUNTY',barmode='group')
plotly4.show()

plotly5 = px.bar(dailySpecific,x='DATESTAMP_MOD_DAY', y='H_Cum', color='COUNTY',barmode='group')
plotly5.show()

plotly6 = px.bar(dailySpecific, x='DATESTAMP_MOD_DAY', y='D_New', color='COUNTY',barmode='group')
plotly6.show()

plotly7 = px.bar(dailySpecific,x='DATESTAMP_MOD_DAY', y='D_Cum', color='COUNTY',barmode='group')
plotly7.show()

dailySpecific['newHospandDeathCovid'] = dailySpecific['D_New'].astype(int) + dailySpecific['H_New'].astype(int) + dailySpecific['C_New'].astype(int)
dailySpecific['newHospandDeathCovid']

dailySpecific['newHospandDeath'] = dailySpecific['D_New'].astype(int) + dailySpecific['H_New'].astype(int)
dailySpecific['newHospandDeath']
dailySpecific

plotly8 = px.bar(dailySpecific,
                 x='DATESTAMP_MOD_DAY',
                 y='newHospandDeathCovid',
                 color='COUNTY',
                 title='Georgia 2020 COVID Data: New Hospitalizations, Deaths, and COVID cases by County',
                 labels={
                     'DATESTAMP_MOD_DAY': "Time (Month, Day, Year)",
                     'newHospandDeathCovid': "Total Count"
                 },
                 barmode='group')
plotly8.update_layout(
    xaxis=dict(
        tickmode='linear',
        type='category'
    )
)
plotly8.show()
