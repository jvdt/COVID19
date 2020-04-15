# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 21:52:53 2020

@author: jvand
"""





#Import library's
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import date
from datetime import timedelta



link_confirmed = "https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
link_deaths    = "https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
link_recovered = "https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"


file_confirmed = link_confirmed.split('/')[-1]
file_deaths    = link_deaths.split('/')[-1]
str_recovered  = requests.get(link_recovered)

response_confirmed  = requests.get(link_confirmed,stream=True)
response_deaths     = requests.get(link_deaths,stream=True)
response_recovered  = requests.get(link_recovered,stream=True)

totalbits               = 0

print(file_confirmed)
if response_confirmed.status_code == 200:
    with open(file_confirmed, 'wb') as f:
        for chunk in response_confirmed.iter_content(chunk_size=1024):
            if chunk:
                totalbits += 1024
                print("Downloaded",totalbits*1025, "KB...")
                f.write(chunk)
    df_confirmed = pd.read_csv(file_confirmed)


df_confirmed = pd.read_csv(str_confirmed, sep=",", skiprows=[1])
df_deaths    = pd.read_csv(str_deaths.text   , sep=",", skiprows=[1])
df_recovered = pd.read_csv(StringIO(str_recovered.text), sep=",", skiprows=[1])

df_confirmed_01 = df_confirmed.groupby('Date')['Value'].sum()
df_deaths_01    = df_deaths.groupby('Date')['Value'].sum()
#df_recovered_01 = df_recovered.groupby('Date')['Value'].sum()




Max_Date = max(df_confirmed['Date'])
Max_Date = datetime.datetime.strptime(Max_Date, '%Y-%m-%d')


df_confirmed['Date'] = pd.to_datetime(df_confirmed['Date'], format='%Y-%m-%d')

plt.plot(df_confirmed_01)
plt.plot(df_deaths_01)
plt.plot(df_recovered_01)
plt.show()

df_confirmed=df_confirmed.fillna(value='')
df_confirmed['Locatie']=df_confirmed['Province/State'].astype('string')+'_'+df_confirmed['Country/Region'].astype('string')


df_confirmed_ordered=df_confirmed.loc[df_confirmed['Date'] == Max_Date].sort_values(by='Value',ascending=False)

df_confirmed_ordered=df_confirmed_ordered.reset_index().drop('index', axis=1)


# plot top 10 locations (combination of first two columns)

for i in range(1,30): 
    actualloc=df_confirmed_ordered['Locatie'].iloc[i]
    df_plot=df_confirmed[df_confirmed['Locatie']==actualloc].sort_values(by='Date')
    plt.plot(df_plot['Date'],df_plot['Value'])

plt.savefig('top 30 excl Huwan China.jpg', dpi='figure')








