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


df_ecdc_Continent = df_ecdc.groupby(['Continent'])['Cases','Deaths'].sum()


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

fig = plt.figure()
ax1 = plt.subplot2grid((3, 2), (0, 0))
ax2 = plt.subplot2grid((3, 2), (0, 1))
ax3 = plt.subplot2grid((3, 2), (1, 0))
ax4 = plt.subplot2grid((3, 2), (1, 1))
ax5 = plt.subplot2grid((3, 2), (2, 0))
ax6 = plt.subplot2grid((3, 2), (2, 1))
fig.set_figheight(22)
fig.set_figwidth(18)
fig.suptitle('Europe and The Netherlands\n Chosen startdate Europe: '+FirstDate.strftime("%d-%m-%Y") ,fontsize=22,y=1.08)


ax=ax1
ax.set_title('Cumulative confirmed cases since' + FirstDate.strftime("%d-%m-%Y") ,fontsize=16)
for i in range(first_InOrder,9): 
    actualloc=df_ecdc_ordered['Countries and territories'].iloc[i]
    df_plot=df_ecdc[df_ecdc['Countries and territories']==actualloc].sort_values(by='DateRep')
    if(actualloc == 'Netherlands'):
        ax.plot(df_plot['DateRep'],np.cumsum(df_plot['Cases']), linewidth=4)
    else:
        ax.plot(df_plot['DateRep'],np.cumsum(df_plot['Cases']))
ax1.set_xlabel('Date sinds first infection in Europe')
ax1.set_ylabel('Cumualtive infection cases (confirmed)')
SubPlot_finalization(ax)


ax=ax2
ax.set_title('Cumulative deaths since ' + FirstDate.strftime("%d-%m-%Y"),fontsize=16)
for i in range(first_InOrder,9): 
    actualloc=df_ecdc_ordered['Countries and territories'].iloc[i]
    df_plot=df_ecdc[df_ecdc['Countries and territories']==actualloc].sort_values(by='DateRep')
    if(actualloc == 'Netherlands'):
        ax.plot(df_plot['DateRep'],np.cumsum(df_plot['Deaths']), linewidth=4)
    else:
        ax.plot(df_plot['DateRep'],np.cumsum(df_plot['Deaths']))
ax1.set_xlabel('Date sinds first infection in Europe')
ax1.set_ylabel('Cumualtive infection cases (confirmed)')
SubPlot_finalization(ax)



#Cumulative from day zero in europe
ax=ax3
ax.set_title('Cumulative confirmed cases since first case in country',fontsize=16)
for i in range(first_InOrder,last__Inorder): 
    actualloc=df_ecdc_ordered['Countries and territories'].iloc[i]
    df_plot=df_ecdc[df_ecdc['Countries and territories']==actualloc].sort_values(by='DateRep')
    FirstDate = df_plot[df_plot['Cases']>0]['DateRep'].min()
    df_plot = df_plot.loc[(df_plot['DateRep'] >= FirstDate)]
    df_plot.reset_index(inplace=True)
    df_plot.reset_index(inplace=True)
    cumcases = np.cumsum(df_plot['Cases'])
   
    if(actualloc=='Netherlands'):
        ax.plot(df_plot['level_0'],np.log10(cumcases), linewidth=4)
    else:
        ax.plot(df_plot['level_0'],np.log10(cumcases)) 
SubPlot_finalization(ax)
ax.set_yscale('log')


#Cumulative from day zero in europe deaths
ax=ax4
ax.set_title('Cumulative confirmed deaths since first in country',fontsize=16)
for i in range(first_InOrder,last__Inorder): 
    actualloc=df_ecdc_ordered['Countries and territories'].iloc[i]
    df_plot=df_ecdc[df_ecdc['Countries and territories']==actualloc].sort_values(by='DateRep')
    FirstDate = df_plot[df_plot['Deaths']>0]['DateRep'].min()
    df_plot = df_plot.loc[(df_plot['DateRep'] >= FirstDate)]
    df_plot.reset_index(inplace=True)
    df_plot.reset_index(inplace=True)
    cumdeaths = np.cumsum(df_plot['Deaths'])
       
    if(actualloc=='Netherlands'):
        ax.plot(df_plot['level_0'],np.log10(cumdeaths), linewidth=4)
    else:
        ax.plot(df_plot['level_0'],np.log10(cumdeaths)) 
SubPlot_finalization(ax)
ax.set_yscale('log')


ax=ax5
ax.set_title('Infectionrate on confirmed cases (n-1)',fontsize=16)
for i in range(first_InOrder,last__Inorder): 
    actualloc=df_ecdc_ordered['Countries and territories'].iloc[i]
    df_plot=df_ecdc[df_ecdc['Countries and territories']==actualloc].sort_values(by='DateRep')
    FirstDate = df_plot[df_plot['Cases']>0]['DateRep'].min()
    df_plot = df_plot.loc[(df_plot['DateRep'] >= FirstDate- timedelta(1))]
    df_plot.reset_index(inplace=True)
    df_plot.reset_index(inplace=True)
    
    CasusCum =np.cumsum(df_plot['Cases'])
    
    if(actualloc=='Netherlands'):
        ax.plot(df_plot['level_0'],CasusCum/CasusCum.shift(1,fill_value=0), linewidth=4)
    else:
        ax.plot(df_plot['level_0'],CasusCum/CasusCum.shift(1,fill_value=0))
ax.set_ylim([0, 2])    
ax.hlines(1,0,30,linestyles='dashed',label ='Growth',colors='r')
SubPlot_finalization(ax)



#death rate
ax=ax6
ax.set_title('Cumulative deathrate on confirmed (!?!) cases',fontsize=16)
for i in range(first_InOrder,last__Inorder): 
    actualloc=df_ecdc_ordered['Countries and territories'].iloc[i]
    df_plot=df_ecdc[df_ecdc['Countries and territories']==actualloc].sort_values(by='DateRep')
    FirstDate = df_plot[df_plot['Cases']>0]['DateRep'].min()
    df_plot = df_plot.loc[(df_plot['DateRep'] >= FirstDate)]
    df_plot.reset_index(inplace=True)
    df_plot.reset_index(inplace=True)
    if(actualloc=='Netherlands'):
        ax.plot(df_plot['level_0'],np.cumsum(df_plot['Deaths'])/np.cumsum(df_plot['Cases']), linewidth=4)
    else:
         ax.plot(df_plot['level_0'],np.cumsum(df_plot['Deaths'])/np.cumsum(df_plot['Cases']))
SubPlot_finalization(ax)





#plt.tight_layout(pad=0.4, w_pad=1, h_pad=2.0)

plt.subplots_adjust(top=0.88)
plt.tight_layout()
plt.savefig('chart_Europe.jpg', dpi='figure' ,bbox_inches='tight')
