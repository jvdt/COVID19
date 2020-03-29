# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 16:20:03 2020

@author: jvand
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import date
from datetime import timedelta

#https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide
#https://www.geonames.org/countries/

today = (date.today()- timedelta(2))

strLinkStart = 'https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-'
strLinkYear  = today.strftime("%Y") 
strLinkMonth = today.strftime("%m")
strLinkday   = today.strftime("%d")
strLinkEnd   = '.xls'

link_ecdc = strLinkStart+strLinkYear+'-'+strLinkMonth+'-'+strLinkday+strLinkEnd
link_ecdc
#link_ecdc = 'https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-2020-03-18.xls'

response  = requests.get(link_ecdc,stream=True)

file_ecdc = link_ecdc.split('/')[-1]
file_GeoId = 'GeoId.xls'

totalbits = 0

if response.status_code == 200:
    with open(file_ecdc, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                totalbits += 1024
                print("Downloaded", totalbits*1025, "KB...")
                f.write(chunk)



df_ecdc = pd.read_excel(file_ecdc)
df_GeoId = pd.read_excel(file_GeoId)

df_GeoId=df_GeoId.rename(columns={"ISO-3166-alpha2": "GeoId"})
   

df_ecdc = pd.merge(df_ecdc,
                 df_GeoId,
                 on='GeoId')


# Dataprep and from here use df_ecdc_basis as startingpoint.
df_ecdc_basis=df_ecdc[df_ecdc['Continent']=='EU']

df_ecdc_groupby = df_ecdc_basis.groupby(['Countries and territories','GeoId'])['Cases','Deaths'].sum()
df_ecdc_ordered = df_ecdc_groupby.sort_values(by=['Cases','Deaths'],ascending=False)
df_ecdc_ordered.name = 'Countries and territories'
df_ecdc_ordered.reset_index(inplace=True)









plt.figure(figsize=[13,13])


for i in range(0,9): 
    actualloc=df_ecdc_ordered['Countries and territories'].iloc[i]
    #actualloc = 'Netherlands'
    df_plot=df_ecdc[df_ecdc['Countries and territories']==actualloc].sort_values(by='DateRep')
    plt.plot(df_plot['DateRep'],df_plot['Cases'])

plt.xticks(rotation=90)
plt.legend(df_ecdc_ordered['Countries and territories'].iloc[0:9])
plt.title("Number of new confirmed cases",fontdict ={'fontsize':'28'})
plt.savefig('Europe_New_Conf_Cases.jpg', dpi='figure')


#cumulatief

plt.figure(figsize=[13,13])

for i in range(0,9): 
    actualloc=df_ecdc_ordered['Countries and territories'].iloc[i]
    #actualloc = 'Netherlands'
    df_plot=df_ecdc[df_ecdc['Countries and territories']==actualloc].sort_values(by='DateRep')
    plt.plot(df_plot['DateRep'],np.cumsum(df_plot['Cases']))

plt.xticks(rotation=90)
plt.legend(df_ecdc_ordered['Countries and territories'].iloc[0:9])
plt.title("Cum number of new confirmed cases",fontdict ={'fontsize':'28'})
plt.savefig('Europe_New_Conf_Cases_Cum.jpg', dpi='figure')



df_ecdc_groupby = df_ecdc_basis.groupby(['Countries and territories','GeoId'])['Cases','Deaths'].sum()


df_ecdc_basis_number = df_ecdc_basis.groupby(['DateRep'])['Cases','Deaths'].sum()
df_ecdc_basis_number['DateRep'] = df_ecdc_basis_number.index
FirstDate = df_ecdc_basis_number[df_ecdc_basis_number['Cases']==0]['DateRep'].max()
df_ecdc = df_ecdc_basis.loc[(df_ecdc_basis['DateRep'] >= FirstDate)]



plt.figure(figsize=[13,13])

for i in range(0,9): 
    actualloc=df_ecdc_ordered['Countries and territories'].iloc[i]
    #actualloc = 'Netherlands'
    df_plot=df_ecdc[df_ecdc['Countries and territories']==actualloc].sort_values(by='DateRep')
    plt.plot(df_plot['DateRep'],np.cumsum(df_plot['Cases']))

plt.xticks(rotation=90)
plt.legend(df_ecdc_ordered['Countries and territories'].iloc[0:9])
plt.title("Cum number of new confirmed cases",fontdict ={'fontsize':'28'})
plt.savefig('Europe_New_Conf_Cases_Cum.jpg', dpi='figure')





#cum from day zero.


plt.figure(figsize=[13,13])

for i in range(0,9): 
    actualloc=df_ecdc_ordered['Countries and territories'].iloc[i]
    df_plot=df_ecdc[df_ecdc['Countries and territories']==actualloc].sort_values(by='DateRep')
    FirstDate = df_plot[df_plot['Cases']>0]['DateRep'].min()
    df_plot = df_plot.loc[(df_plot['DateRep'] >= FirstDate)]
    df_plot.reset_index(inplace=True)
    df_plot.reset_index(inplace=True)
    plt.plot(df_plot['level_0'],np.cumsum(df_plot['Cases']))

plt.xticks(rotation=90)
plt.legend(df_ecdc_ordered['Countries and territories'].iloc[0:9])
plt.title("Cum number of new confirmed cases",fontdict ={'fontsize':'28'})
plt.savefig('Europe_New_Conf_Cases_Cum_From_day_0.jpg', dpi='figure')


#death rate


plt.figure(figsize=[13,13])

for i in range(0,9): 
    actualloc=df_ecdc_ordered['Countries and territories'].iloc[i]
    df_plot=df_ecdc[df_ecdc['Countries and territories']==actualloc].sort_values(by='DateRep')
    FirstDate = df_plot[df_plot['Cases']>0]['DateRep'].min()
    df_plot = df_plot.loc[(df_plot['DateRep'] >= FirstDate)]
    df_plot.reset_index(inplace=True)
    df_plot.reset_index(inplace=True)
    plt.plot(df_plot['level_0'],np.cumsum(df_plot['Deaths'])/np.cumsum(df_plot['Cases']))

plt.xticks(rotation=90)
plt.legend(df_ecdc_ordered['Countries and territories'].iloc[0:9])
plt.title("Death rate on cum conf cases",fontdict ={'fontsize':'28'})
plt.savefig('Europe_Death_rate_on_Conf_Cases_Cum_From_day_0.jpg', dpi='figure')



plt.figure(figsize=[13,13])

for i in range(0,9): 
    actualloc=df_ecdc_ordered['Countries and territories'].iloc[i]
    df_plot=df_ecdc[df_ecdc['Countries and territories']==actualloc].sort_values(by='DateRep')
    FirstDate = df_plot[df_plot['Cases']>0]['DateRep'].min()
    df_plot = df_plot.loc[(df_plot['DateRep'] >= FirstDate)]
    df_plot.reset_index(inplace=True)
    df_plot.reset_index(inplace=True)
    plt.plot(df_plot['level_0'],np.cumsum(df_plot['Cases']))

plt.xticks(rotation=90)
plt.yscale("Log")
plt.legend(df_ecdc_ordered['Countries and territories'].iloc[0:9])
plt.title("Cum number of new confirmed cases",fontdict ={'fontsize':'28'})
plt.savefig('Europe_New_Conf_Cases_Cum_From_day_0_logscale.jpg', dpi='figure')

