# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 16:20:03 2020

@author: jvand
"""

import requests
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from datetime import date
from datetime import timedelta

#https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide
#https://www.geonames.org/countries/

today = (date.today()- timedelta(0))

strLinkStart = 'https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-'
strLinkYear  = today.strftime("%Y") 
strLinkMonth = today.strftime("%m")
strLinkday   = today.strftime("%d")
strLinkEnd   = '.xlsx'

link_ecdc = strLinkStart+strLinkYear+'-'+strLinkMonth+'-'+strLinkday+strLinkEnd
link_ecdc
#link_ecdc = 'https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-2020-03-18.xls'

response  = requests.get(link_ecdc,stream=True)

file_ecdc = link_ecdc.split('/')[-1]
file_GeoId = 'GeoId.xls'
first_InOrder = 0
last__Inorder = 9


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


df_ecdc_groupby = df_ecdc_basis.groupby(['Countries and territories','GeoId'])['Cases','Deaths'].sum()


df_ecdc_basis_number = df_ecdc_basis.groupby(['DateRep'])['Cases','Deaths'].sum()
df_ecdc_basis_number['DateRep'] = df_ecdc_basis_number.index
FirstDate = df_ecdc_basis_number[df_ecdc_basis_number['Cases']==0]['DateRep'].max()
df_ecdc = df_ecdc_basis.loc[(df_ecdc_basis['DateRep'] >= FirstDate)]



def SubPlot_finalization(ax):
    ax.set_axisbelow(True)
    ax.minorticks_on()
    ax.grid(which='major', linestyle='-', linewidth='0.7', color='black')
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    ax.legend(df_ecdc_ordered['Countries and territories'].iloc[first_InOrder:last__Inorder])
    


#plot prep

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
fig.suptitle('Europe and The Netherlands\n Chosen startdate Europe: '+FirstDate.strftime("%d")+'-'+FirstDate.strftime("%m")+ '-' +FirstDate.strftime("%Y") ,fontsize=22)
fig.set_figheight(13)
fig.set_figwidth(13)



ax1.set_title('Cumulative confirmed cases from first in Europe',fontsize=14)
for i in range(first_InOrder,9): 
    actualloc=df_ecdc_ordered['Countries and territories'].iloc[i]
    df_plot=df_ecdc[df_ecdc['Countries and territories']==actualloc].sort_values(by='DateRep')
    if(actualloc == 'Netherlands'):
        ax1.plot(df_plot['DateRep'],np.cumsum(df_plot['Cases']), linewidth=4)
    else:
        ax1.plot(df_plot['DateRep'],np.cumsum(df_plot['Cases']))
ax1.set_xlabel('Date sinds first infection in Europe')
ax1.set_ylabel('Cumualtive infection cases (confirmed)')
SubPlot_finalization(ax1)




#Cumulative from day zero in europe
ax2.set_title('Cumulative confirmed cases from first in country',fontsize=14)
for i in range(first_InOrder,last__Inorder): 
    actualloc=df_ecdc_ordered['Countries and territories'].iloc[i]
    df_plot=df_ecdc[df_ecdc['Countries and territories']==actualloc].sort_values(by='DateRep')
    FirstDate = df_plot[df_plot['Cases']>0]['DateRep'].min()
    df_plot = df_plot.loc[(df_plot['DateRep'] >= FirstDate)]
    df_plot.reset_index(inplace=True)
    df_plot.reset_index(inplace=True)
   
    if(actualloc=='Netherlands'):
        ax2.plot(df_plot['level_0'],np.cumsum(df_plot['Cases']), linewidth=4)
    else:
        ax2.plot(df_plot['level_0'],np.cumsum(df_plot['Cases'])) 
SubPlot_finalization(ax2)



ax3.set_title('Infectionrate on confirmed cases (n-1)',fontsize=14)
for i in range(first_InOrder,last__Inorder): 
    actualloc=df_ecdc_ordered['Countries and territories'].iloc[i]
    df_plot=df_ecdc[df_ecdc['Countries and territories']==actualloc].sort_values(by='DateRep')
    FirstDate = df_plot[df_plot['Cases']>0]['DateRep'].min()
    df_plot = df_plot.loc[(df_plot['DateRep'] >= FirstDate- timedelta(1))]
    df_plot.reset_index(inplace=True)
    df_plot.reset_index(inplace=True)
    
    CasusCum =np.cumsum(df_plot['Cases'])
    
    if(actualloc=='Netherlands'):
        ax3.plot(df_plot['level_0'],CasusCum/CasusCum.shift(1,fill_value=0), linewidth=4)
    else:
        ax3.plot(df_plot['level_0'],CasusCum/CasusCum.shift(1,fill_value=0))
ax3.set_ylim([0, 2])    
ax3.hlines(1,0,30,linestyles='dashed',label ='Growth',colors='r')
SubPlot_finalization(ax3)


#death rate
ax4.set_title('Deathrate on confirmed cases, cumulative',fontsize=14)
for i in range(first_InOrder,last__Inorder): 
    actualloc=df_ecdc_ordered['Countries and territories'].iloc[i]
    df_plot=df_ecdc[df_ecdc['Countries and territories']==actualloc].sort_values(by='DateRep')
    FirstDate = df_plot[df_plot['Cases']>0]['DateRep'].min()
    df_plot = df_plot.loc[(df_plot['DateRep'] >= FirstDate)]
    df_plot.reset_index(inplace=True)
    df_plot.reset_index(inplace=True)
    if(actualloc=='Netherlands'):
        ax4.plot(df_plot['level_0'],np.cumsum(df_plot['Deaths'])/np.cumsum(df_plot['Cases']), linewidth=4)
    else:
         ax4.plot(df_plot['level_0'],np.cumsum(df_plot['Deaths'])/np.cumsum(df_plot['Cases']))
SubPlot_finalization(ax4)



plt.savefig('Europe.jpg', dpi='figure')
