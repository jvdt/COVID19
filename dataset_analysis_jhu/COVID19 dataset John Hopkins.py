# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 21:52:53 2020

@author: jvand
"""





#Import library's
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import date
from datetime import timedelta
import os

first_InOrder = 0
last__Inorder = 15

#dir_base = './dataset_analysis_jhu/'

downloadNew=False


link_confirmed = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
link_deaths    = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
link_recovered = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"


#file_confirmed = dir_base+link_confirmed.split('/')[-1]
#file_deaths    = dir_base+link_deaths.split('/')[-1]
#file_recovered = dir_base+link_recovered.split('/')[-1]


file_confirmed = link_confirmed.split('/')[-1]
file_deaths    = link_deaths.split('/')[-1]
file_recovered = link_recovered.split('/')[-1]
    
if(downloadNew==True):
    
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
    
    totalbits               = 0
    print(file_deaths)
    if response_deaths.status_code == 200:
        with open(file_deaths, 'wb') as f:
            for chunk in response_deaths.iter_content(chunk_size=1024):
                if chunk:
                    totalbits += 1024
                    print("Downloaded",totalbits*1025, "KB...")
                    f.write(chunk)
    
    totalbits               = 0
    print(file_recovered)
    if response_recovered.status_code == 200:
        with open(file_recovered, 'wb') as f:
            for chunk in response_recovered.iter_content(chunk_size=1024):
                if chunk:
                    totalbits += 1024
                    print("Downloaded",totalbits*1025, "KB...")
                    f.write(chunk)

#end of download

df_confirmed  = pd.read_csv(file_confirmed)
df_deaths     = pd.read_csv(file_deaths)
df_recovered  = pd.read_csv(file_recovered)


MinimumCases =10
#df_confirmed_01 = df_confirmed.groupby('Date')['Value'].sum()
#df_deaths_01    = df_deaths.groupby('Date')['Value'].sum()
#df_recovered_01 = df_recovered.groupby('Date')['Value'].sum()


df_confirmed_ordered = df_confirmed.sort_values(   by=df_confirmed.columns[len(df_confirmed.columns)-1],ascending=False)
df_deaths_ordered    = df_deaths.reindex(df_confirmed_ordered.index)
df_recovered_ordered = df_recovered.reindex(df_confirmed_ordered.index)

#print(df_confirmed_ordered.head())
#print(df_deaths_ordered.head())
#print(df_recovered_ordered.head())


maxAxisX=101

def SubPlot_finalization_isDate(ax,df,first,last):
    #major_ticks = np.arange(0, maxAxisX, 20)
    #minor_ticks = np.arange(0, 101, 5)
    ax.set_axisbelow(True)
    ax.minorticks_on()
    ax.grid(which='major', linestyle='-', linewidth='0.25', color='grey',alpha=0.5)
    #ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    ax.legend(df['Country/Region'].iloc[first:last])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    #ax.set_xticks(major_ticks)


def SubPlot_finalization_nonDate(ax,df,first,last):
    major_ticks = np.arange(0, maxAxisX, 20)
    #minor_ticks = np.arange(0, 101, 5)
    ax.set_axisbelow(True)
    ax.minorticks_on()
    ax.grid(which='major', linestyle='-', linewidth='0.25', color='grey',alpha=0.5)
    #ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    ax.legend(df['Country/Region'].iloc[first:last])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xticks(major_ticks)



    
   
fig = plt.figure()
ax1 = plt.subplot2grid((3, 2), (0, 0),)
ax2 = plt.subplot2grid((3, 2), (0, 1))
ax3 = plt.subplot2grid((3, 2), (1, 0))
ax4 = plt.subplot2grid((3, 2), (1, 1))
ax5 = plt.subplot2grid((3, 2), (2, 0))
ax6 = plt.subplot2grid((3, 2), (2, 1))
fig.set_figheight(22)
fig.set_figwidth(18)
#fig.suptitle('Wereldwijd \n First case: '+FirstDate.strftime("%d-%m-%Y")+'\n'+'ECDC data update: '+today.strftime("%d-%m-%Y") ,fontsize=22,y=1.08)
fig.suptitle('Wereldwijd',fontsize=22,y=1.08)
left = 0.125  # the left side of the subplots of the figure
right = 0.9   # the right side of the subplots of the figure
bottom = 0.1  # the bottom of the subplots of the figure
top = 0.9     # the top of the subplots of the figure
wspace = 0.2  # the amount of width reserved for space between subplots,
              # expressed as a fraction of the average axis width
hspace = 0.2  # the amount of height reserved for space between subplots,
              # expressed as a fraction of the average axis height
fig.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)


#+ FirstDate.strftime("%d-%m-%Y")
ax=ax1
ax.set_title('cumulative confirmed cases'  ,fontsize=16)
for i in range(first_InOrder,last__Inorder): 
    df_plot = df_confirmed_ordered.iloc[i][4:len(df_confirmed_ordered.columns)].reset_index()
    df_plot.columns=['Date','Country']
    df_plot['Date']=pd.to_datetime(df_plot['Date'])
    ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
    ax.plot(pd.to_datetime(df_plot['Date']),df_plot['Country'])
ax.set_xlabel('Date since first infection')
ax.set_ylabel('Cumualtive infection cases (confirmed)')
SubPlot_finalization_isDate(ax,df_confirmed_ordered,first_InOrder,last__Inorder)
print('Plot 1')


ax=ax2
ax.set_title('cumulative deaths',fontsize=16)
for i in range(first_InOrder,last__Inorder): 
    df_plot=df_deaths_ordered.iloc[i][4:len(df_deaths_ordered.columns)].reset_index()
    df_plot.columns=['Date','Country']
    df_plot['Date']=pd.to_datetime(df_plot['Date'])
    ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
    ax.plot(pd.to_datetime(df_plot['Date']),df_plot['Country'])
ax.set_xlabel('Date sinds first infection')
ax.set_ylabel('Cumualtive infection cases (confirmed)')
SubPlot_finalization_isDate(ax,df_deaths_ordered,first_InOrder,last__Inorder)
print('Plot 2')

ax=ax3
ax.set_title('Cumulative confirmed cases since first case in country',fontsize=16)
for i in range(first_InOrder,last__Inorder): 
    df_plot=df_confirmed_ordered.iloc[i][4:len(df_confirmed_ordered.columns)].reset_index()
    df_plot.columns=['Date','Country']
    df_plot['Date']=pd.to_datetime(df_plot['Date'])
    FirstDateC = df_plot[df_plot['Country']>MinimumCases]['Date'].min()
    df_plot = df_plot.loc[(df_plot['Date'] >= FirstDateC)]
    df_plot.reset_index(inplace=True)
    df_plot.reset_index(inplace=True)
    ax.plot(df_plot['level_0'],df_plot['Country'])
SubPlot_finalization_nonDate(ax,df_confirmed_ordered,first_InOrder,last__Inorder)
ax.set_yscale('log')
print('Plot 3')


ax=ax4
ax.set_title('Cumulative confirmed cases since first case in country',fontsize=16)
for i in range(first_InOrder,last__Inorder): 
    df_plot=df_deaths_ordered.iloc[i][4:len(df_deaths_ordered.columns)].reset_index()
    df_plot.columns=['Date','Country']
    df_plot['Date']=pd.to_datetime(df_plot['Date'])
    FirstDateC = df_plot[df_plot['Country']>MinimumCases]['Date'].min()
    df_plot = df_plot.loc[(df_plot['Date'] >= FirstDateC)]
    df_plot.reset_index(inplace=True)
    df_plot.reset_index(inplace=True)
    ax.plot(df_plot['level_0'],df_plot['Country'])
SubPlot_finalization_nonDate(ax,df_deaths_ordered,first_InOrder,last__Inorder)
ax.set_yscale('log')
print('Plot 4')

   
ax=ax5
ax.set_title('Infectionrate on confirmed cases (n-1)',fontsize=16)
for i in range(first_InOrder,last__Inorder): 
    df_plot=df_confirmed_ordered.iloc[i][4:len(df_confirmed_ordered.columns)].reset_index()
    df_plot.columns=['Date','Country']
    df_plot['Date']=pd.to_datetime(df_plot['Date'])
    FirstDate5 = df_plot[df_plot['Country']>MinimumCases]['Date'].min()
    df_plot = df_plot.loc[(df_plot['Date'] >= (FirstDate5- timedelta(1)))]
   
    df_plot.reset_index(inplace=True)
    df_plot.reset_index(inplace=True)    
    ax.plot(df_plot['level_0'],df_plot['Country']/df_plot['Country'].shift(1,fill_value=0))
ax.set_ylim([0,2])    
ax.hlines(1,0,maxAxisX,linestyles='dashed',label ='Growth',colors='r')
SubPlot_finalization_nonDate(ax,df_confirmed_ordered,first_InOrder,last__Inorder)
print('Plot 5')


ax=ax6
ax.set_title('Deathrate as fraction of death and recovered',fontsize=16)
for i in range(first_InOrder,last__Inorder): 
    #deaths
    df_plot = df_deaths_ordered.iloc[i][4:len(df_deaths_ordered.columns)].reset_index()
    df_plot.columns=['Date','Deaths']
    
    #recovered
    df_plot_r = df_recovered_ordered.iloc[i][4:len(df_recovered_ordered.columns)].reset_index()
    df_plot_r.columns=['Date','Recovered']

    df_plot=df_plot.merge(df_plot_r,on='Date')

    #confirmed
    df_plot_r = df_confirmed_ordered.iloc[i][4:len(df_confirmed_ordered.columns)].reset_index()
    df_plot_r.columns=['Date','Confirmed']

    df_plot = df_plot.merge(df_plot_r,on='Date')
    
    df_plot['Date'] = pd.to_datetime(df_plot['Date'])
    
    
    FirstDateC = df_plot[df_plot['Deaths']+df_plot['Recovered']>MinimumCases]['Date'].min()
    df_plot = df_plot.loc[(df_plot['Date'] >= FirstDateC)]
    df_plot.reset_index(inplace=True)
    df_plot.reset_index(inplace=True)    
    
    ax.plot(df_plot['level_0'],df_plot['Deaths']/(df_plot['Recovered']+df_plot['Deaths'])) 
SubPlot_finalization_nonDate(ax,df_deaths_ordered,first_InOrder,last__Inorder)

print('Plot 6')

#plt.tight_layout(pad=0.4, w_pad=1, h_pad=2.0)
#plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
#plt.subplots_adjust(top=0.88)
plt.tight_layout(pad=0.9,h_pad=0.8)
plt.savefig('chart_World.jpg', dpi='figure' ,bbox_inches='tight')
print('Plot saved')









