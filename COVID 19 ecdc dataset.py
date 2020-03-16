# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 16:20:03 2020

@author: jvand
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt


link_ecdc = 'https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-2020-03-15.xls'

response  = requests.get(link_ecdc,stream=True)

local_filename = link_ecdc.split('/')[-1]
totalbits = 0

if response.status_code == 200:
    with open(local_filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                totalbits += 1024
                print("Downloaded", totalbits*1025, "KB...")
                f.write(chunk)



df_ecdc = pd.read_excel(local_filename)



df_ecdc_groupby = df_ecdc.groupby(['CountryExp','EU','GeoId'])['NewConfCases','NewDeaths'].sum()
df_ecdc_ordered = df_ecdc_groupby.sort_values(by=['NewConfCases','NewDeaths'],ascending=False)
df_ecdc_ordered.name = 'CountryExp'
df_ecdc_ordered.reset_index(inplace=True)




plt.figure(figsize=[15,15])

for i in range(1,12): 
    actualloc=df_ecdc_ordered['CountryExp'].iloc[i]
    #actualloc = 'Netherlands'
    df_plot=df_ecdc[df_ecdc['CountryExp']==actualloc].sort_values(by='DateRep')
    plt.plot(df_plot['DateRep'],df_plot['NewConfCases'])

plt.xticks(rotation=90)
plt.legend(df_ecdc_ordered['CountryExp'].iloc[1:12])
plt.title("Number of new confirmed cases",fontdict ={'fontsize':'28'})
plt.savefig('Europa.jpg', dpi='figure')







