# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 21:52:53 2020

@author: jvand
"""




import requests
from io import StringIO
import pandas as pd
import matplotlib.pyplot as plt
import datetime 


link_confirmed = "https://proxy.hxlstandard.org/data/download/time_series-ncov-Confirmed.csv?dest=data_edit&filter01=explode&explode-header-att01=date&explode-value-att01=value&filter02=rename&rename-oldtag02=%23affected%2Bdate&rename-newtag02=%23date&rename-header02=Date&filter03=rename&rename-oldtag03=%23affected%2Bvalue&rename-newtag03=%23affected%2Binfected%2Bvalue%2Bnum&rename-header03=Value&filter04=clean&clean-date-tags04=%23date&filter05=sort&sort-tags05=%23date&sort-reverse05=on&filter06=sort&sort-tags06=%23country%2Bname%2C%23adm1%2Bname&tagger-match-all=on&tagger-default-tag=%23affected%2Blabel&tagger-01-header=province%2Fstate&tagger-01-tag=%23adm1%2Bname&tagger-02-header=country%2Fregion&tagger-02-tag=%23country%2Bname&tagger-03-header=lat&tagger-03-tag=%23geo%2Blat&tagger-04-header=long&tagger-04-tag=%23geo%2Blon&header-row=1&url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_19-covid-Confirmed.csv"
link_deaths    = "https://proxy.hxlstandard.org/data/download/time_series-ncov-Deaths.csv?dest=data_edit&filter01=explode&explode-header-att01=date&explode-value-att01=value&filter02=rename&rename-oldtag02=%23affected%2Bdate&rename-newtag02=%23date&rename-header02=Date&filter03=rename&rename-oldtag03=%23affected%2Bvalue&rename-newtag03=%23affected%2Bkilled%2Bvalue%2Bnum&rename-header03=Value&filter04=clean&clean-date-tags04=%23date&filter05=sort&sort-tags05=%23date&sort-reverse05=on&filter06=sort&sort-tags06=%23country%2Bname%2C%23adm1%2Bname&tagger-match-all=on&tagger-default-tag=%23affected%2Blabel&tagger-01-header=province%2Fstate&tagger-01-tag=%23adm1%2Bname&tagger-02-header=country%2Fregion&tagger-02-tag=%23country%2Bname&tagger-03-header=lat&tagger-03-tag=%23geo%2Blat&tagger-04-header=long&tagger-04-tag=%23geo%2Blon&header-row=1&url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_19-covid-Deaths.csv"
link_recovered = "https://proxy.hxlstandard.org/data/download/time_series-ncov-Recovered.csv?dest=data_edit&filter01=explode&explode-header-att01=date&explode-value-att01=value&filter02=rename&rename-oldtag02=%23affected%2Bdate&rename-newtag02=%23date&rename-header02=Date&filter03=rename&rename-oldtag03=%23affected%2Bvalue&rename-newtag03=%23affected%2Brecovered%2Bvalue%2Bnum&rename-header03=Value&filter04=clean&clean-date-tags04=%23date&filter05=sort&sort-tags05=%23date&sort-reverse05=on&filter06=sort&sort-tags06=%23country%2Bname%2C%23adm1%2Bname&tagger-match-all=on&tagger-default-tag=%23affected%2Blabel&tagger-01-header=province%2Fstate&tagger-01-tag=%23adm1%2Bname&tagger-02-header=country%2Fregion&tagger-02-tag=%23country%2Bname&tagger-03-header=lat&tagger-03-tag=%23geo%2Blat&tagger-04-header=long&tagger-04-tag=%23geo%2Blon&header-row=1&url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_19-covid-Recovered.csv"

str_confirmed  = requests.get(link_confirmed)
str_deaths     = requests.get(link_deaths)
str_recovered  = requests.get(link_recovered)

df_confirmed = pd.read_csv(StringIO(str_confirmed.text), sep=",", skiprows=[1])
df_deaths    = pd.read_csv(StringIO(str_deaths.text)   , sep=",", skiprows=[1])
df_recovered = pd.read_csv(StringIO(str_recovered.text), sep=",", skiprows=[1])

df_confirmed_01 = df_confirmed.groupby('Date')['Value'].sum()
df_deaths_01    = df_deaths.groupby('Date')['Value'].sum()
df_recovered_01 = df_recovered.groupby('Date')['Value'].sum()

Max_Date = max(df_confirmed['Date'])
Max_Date = datetime.datetime.strptime(Max_Date, '%Y-%m-%d')


df_confirmed['Date'] = pd.to_datetime(df_confirmed['Date'], format='%Y-%m-%d')

plt.plot(df_confirmed_01)
plt.plot(df_deaths_01)
plt.plot(df_recovered_01)
plt.show()

df_confirmed=df_confirmed.fillna(value='')
df_confirmed['Locatie']=df_confirmed['Province/State'].astype('string')+df_confirmed['Country/Region'].astype('string')


df_confirmed_ordered=df_confirmed.loc[df_confirmed['Date'] == Max_Date].sort_values(by='Value',ascending=False)

df_confirmed_ordered=df_confirmed_ordered.reset_index().drop('index', axis=1)




for i in range(2,6): 
    actualloc=df_confirmed_ordered['Locatie'].iloc[i]
    df_plot=df_confirmed[df_confirmed['Locatie']==actualloc].sort_values(by='Date')
    plt.plot(df_plot['Date'],df_plot['Value'])










