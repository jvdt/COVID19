"""
Created on Sun Mar 15 16:20:03 2020
###### -*- coding: utf-8 -*-

Data sources:    
#https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide
#https://www.geonames.org/countries/

@author: jvand
"""


#Import library's
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import date
from datetime import timedelta




def SubPlot_finalization(ax,df,first,last):
    ax.set_axisbelow(True)
    ax.minorticks_on()
    ax.grid(which='major', linestyle='-', linewidth='0.7', color='black')
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    ax.legend(df['Countries and territories'].iloc[first:last])
    


def main():
    
    nrDaysBack = 2
    
    today = (date.today()- timedelta(nrDaysBack))
    yesterday = (date.today()- timedelta(nrDaysBack+1))
    
    strLinkStart            = 'https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-'
    strLinkDateToday        = today.strftime("%Y-%m-%d") 
    strLinkDateYesterday    = yesterday.strftime("%Y-%m-%d") 
    strLinkEnd              = '.xlsx'
    
    link_ecdc_today         = strLinkStart+strLinkDateToday+strLinkEnd
    link_ecdc_yesterday     = strLinkStart+strLinkDateYesterday+strLinkEnd
    
    responseToday           = requests.get(link_ecdc_today,stream=True)
    responseYesterday       = requests.get(link_ecdc_yesterday,stream=True)
    
    file_GeoId              = 'GeoId.xls'
    first_InOrder           = 0
    last__Inorder           = 9
    totalbits               = 0
    
    MinimumCases            = 100
        
    file_ecdc_today = link_ecdc_today.split('/')[-1]
    file_ecdc_yesterday = link_ecdc_yesterday.split('/')[-1]
    
    if responseToday.status_code == 200:
        with open(file_ecdc_today, 'wb') as f:
            for chunk in responseToday.iter_content(chunk_size=1024):
                if chunk:
                    totalbits += 1024
                    print("Downloaded", totalbits*1025, "KB...")
                    f.write(chunk)
        df_ecdc = pd.read_excel(file_ecdc_today)
    elif responseYesterday.status_code == 200:
        with open(file_ecdc_yesterday, 'wb') as f:
            for chunk in responseYesterday.iter_content(chunk_size=1024):
                if chunk:
                    totalbits += 1024
                    print("Downloaded", totalbits*1025, "KB...")
                    f.write(chunk)
        df_ecdc = pd.read_excel(file_ecdc_yesterday)
    
    
    df_GeoId = pd.read_excel(file_GeoId)
    df_GeoId = df_GeoId.rename(columns={"ISO-3166-alpha2": "GeoId"})
       
    
    df_ecdc = pd.merge(df_ecdc, df_GeoId, on='GeoId')
    
    
#    df_ecdc_Continent = df_ecdc.groupby('Continent')['Cases','Deaths'].sum()

    df_ecdc_Continent = df_ecdc[['Continent','Cases','Deaths']].groupby('Continent').sum().sort_values(by='Cases', ascending=False)
    df_ecdc_Continent.reset_index(inplace=True)
        

    
    
    # Dataprep and from here use df_ecdc_basis as startingpoint.
    a=0
    print('Start for loop')
    for a in range(0,1): 
        print(a)
        continent = df_ecdc_Continent['Continent'].iloc[a]
        print(continent)
        df_ecdc_basis=df_ecdc[df_ecdc['Continent']==continent]
    
        df_ecdc_ordered = df_ecdc_basis[['Countries and territories','GeoId','Cases','Deaths']].groupby(['Countries and territories','GeoId']).sum().sort_values(by=['Cases','Deaths'],ascending=False)
        #df_ecdc_ordered = df_ecdc_groupby.sort_values(by=['Cases','Deaths'],ascending=False)
        df_ecdc_ordered.name = 'Countries and territories'
        df_ecdc_ordered.reset_index(inplace=True)
    
    
    
        #   df_ecdc_groupby = df_ecdc_basis.groupby(['Countries and territories','GeoId'])['Cases','Deaths'].sum()
    
    
        df_ecdc_basis_number = df_ecdc_basis.groupby(['DateRep'])['Cases','Deaths'].sum()
        df_ecdc_basis_number['DateRep'] = df_ecdc_basis_number.index
        FirstDate = df_ecdc_basis_number[df_ecdc_basis_number['Cases']>0]['DateRep'].min()
        df_ecdc = df_ecdc_basis.loc[(df_ecdc_basis['DateRep'] >= FirstDate)]
        print(FirstDate)
    
    
    
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
        fig.suptitle('Contintent '+ continent + ' \n First case: '+FirstDate.strftime("%d-%m-%Y")+'\n'+'ECDC data update: '+today.strftime("%d-%m-%Y") ,fontsize=22,y=1.08)
        
        
        ax=ax1
        ax.set_title('Cumulative confirmed cases since' + FirstDate.strftime("%d-%m-%Y") ,fontsize=16)
        for i in range(first_InOrder,last__Inorder): 
            actualloc=df_ecdc_ordered['Countries and territories'].iloc[i]
            df_plot=df_ecdc[df_ecdc['Countries and territories']==actualloc].sort_values(by='DateRep')
            if(actualloc == 'Netherlands'):
                ax.plot(df_plot['DateRep'],np.cumsum(df_plot['Cases']), linewidth=4)
            else:
                ax.plot(df_plot['DateRep'],np.cumsum(df_plot['Cases']))
        ax1.set_xlabel('Date sinds first infection in Europe')
        ax1.set_ylabel('Cumualtive infection cases (confirmed)')
        SubPlot_finalization(ax,df_ecdc_ordered,first_InOrder,last__Inorder)
        
        
        ax=ax2
        ax.set_title('Cumulative deaths since ' + FirstDate.strftime("%d-%m-%Y"),fontsize=16)
        for i in range(first_InOrder,last__Inorder): 
            actualloc=df_ecdc_ordered['Countries and territories'].iloc[i]
            df_plot=df_ecdc[df_ecdc['Countries and territories']==actualloc].sort_values(by='DateRep')
            if(actualloc == 'Netherlands'):
                ax.plot(df_plot['DateRep'],np.cumsum(df_plot['Deaths']), linewidth=4)
            else:
                ax.plot(df_plot['DateRep'],np.cumsum(df_plot['Deaths']))
        ax1.set_xlabel('Date sinds first infection in Europe')
        ax1.set_ylabel('Cumualtive infection cases (confirmed)')
        SubPlot_finalization(ax,df_ecdc_ordered,first_InOrder,last__Inorder)
        
        
        
        #Cumulative from day zero in europe
        ax=ax3
        ax.set_title('Cumulative confirmed cases since first case in country',fontsize=16)
        for i in range(first_InOrder,last__Inorder): 
            actualloc=df_ecdc_ordered['Countries and territories'].iloc[i]
            df_plot=df_ecdc[df_ecdc['Countries and territories']==actualloc].sort_values(by='DateRep')
            FirstDateC = df_plot[df_plot['Cases']>MinimumCases]['DateRep'].min()
            df_plot = df_plot.loc[(df_plot['DateRep'] >= FirstDateC)]
            df_plot.reset_index(inplace=True)
            df_plot.reset_index(inplace=True)
            cumcases = np.cumsum(df_plot['Cases'])
           
            if(actualloc=='Netherlands'):
                ax.plot(df_plot['level_0'],np.log10(cumcases), linewidth=4)
            else:
                ax.plot(df_plot['level_0'],np.log10(cumcases)) 
        SubPlot_finalization(ax,df_ecdc_ordered,first_InOrder,last__Inorder)
        ax.set_yscale('log')
        
        
        #Cumulative from day zero in europe deaths
        ax=ax4
        ax.set_title('Cumulative confirmed deaths since first in country',fontsize=16)
        for i in range(first_InOrder,last__Inorder): 
            actualloc=df_ecdc_ordered['Countries and territories'].iloc[i]
            df_plot=df_ecdc[df_ecdc['Countries and territories']==actualloc].sort_values(by='DateRep')
            FirstDateD = df_plot[df_plot['Deaths']>MinimumCases]['DateRep'].min()
            df_plot = df_plot.loc[(df_plot['DateRep'] >= FirstDateD)]
            df_plot.reset_index(inplace=True)
            df_plot.reset_index(inplace=True)
            cumdeaths = np.cumsum(df_plot['Deaths'])
               
            if(actualloc=='Netherlands'):
                ax.plot(df_plot['level_0'],np.log10(cumdeaths), linewidth=4)
            else:
                ax.plot(df_plot['level_0'],np.log10(cumdeaths)) 
        SubPlot_finalization(ax,df_ecdc_ordered,first_InOrder,last__Inorder)
        ax.set_yscale('log')
        
        
        ax=ax5
        ax.set_title('Infectionrate on confirmed cases (n-1)',fontsize=16)
        for i in range(first_InOrder,last__Inorder): 
            actualloc=df_ecdc_ordered['Countries and territories'].iloc[i]
            df_plot=df_ecdc[df_ecdc['Countries and territories']==actualloc].sort_values(by='DateRep')
            FirstDate5 = df_plot[df_plot['Cases']>MinimumCases]['DateRep'].min()
            df_plot = df_plot.loc[(df_plot['DateRep'] >= (FirstDate5- timedelta(1)))]
            df_plot.reset_index(inplace=True)
            df_plot.reset_index(inplace=True)
            
            CasusCum =np.cumsum(df_plot['Cases'])
            
            if(actualloc=='Netherlands'):
                ax.plot(df_plot['level_0'],CasusCum/CasusCum.shift(1,fill_value=0), linewidth=4)
            else:
                ax.plot(df_plot['level_0'],CasusCum/CasusCum.shift(1,fill_value=0))
        ax.set_ylim([0, 2])    
        ax.hlines(1,0,40,linestyles='dashed',label ='Growth',colors='r')
        SubPlot_finalization(ax,df_ecdc_ordered,first_InOrder,last__Inorder)
        
        
        
        #death rate
        ax=ax6
        ax.set_title('Cumulative deathrate on confirmed (!?!) cases',fontsize=16)
        for i in range(first_InOrder,last__Inorder): 
            actualloc=df_ecdc_ordered['Countries and territories'].iloc[i]
            df_plot=df_ecdc[df_ecdc['Countries and territories']==actualloc].sort_values(by='DateRep')
            FirstDate = df_plot[df_plot['Cases']>MinimumCases]['DateRep'].min()
            df_plot = df_plot.loc[(df_plot['DateRep'] >= FirstDate)]
            df_plot.reset_index(inplace=True)
            df_plot.reset_index(inplace=True)
            if(actualloc=='Netherlands'):
                ax.plot(df_plot['level_0'],np.cumsum(df_plot['Deaths'])/np.cumsum(df_plot['Cases']), linewidth=4)
            else:
                 ax.plot(df_plot['level_0'],np.cumsum(df_plot['Deaths'])/np.cumsum(df_plot['Cases']))
        SubPlot_finalization(ax,df_ecdc_ordered,first_InOrder,last__Inorder)
        
        
        
        
        
        #plt.tight_layout(pad=0.4, w_pad=1, h_pad=2.0)
        
        plt.subplots_adjust(top=0.88)
        plt.tight_layout()
        plt.savefig('chart_'+continent+'.jpg', dpi='figure' ,bbox_inches='tight')
    




if __name__ == "__main__":
    main()



