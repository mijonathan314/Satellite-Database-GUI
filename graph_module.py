#!/usr/bin/env python
# coding: utf-8

# In[5]:


import glob
from operator import index
import os
import pandas as pd
from matplotlib import pyplot as plt
import mplcursors
from mplcursors import cursor  
from matplotlib.container import BarContainer
import matplotlib as mpl
get_ipython().run_line_magic('matplotlib', 'qt')


def show_annotation(sel):
    if type(sel.artist) == BarContainer:
        bar = sel.artist[sel.index]
        sel.annotation.set_text(f'{sel.artist.get_label()}: {bar.get_height():.1f}')
        sel.annotation.xy = (bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height() / 2)
        sel.annotation.get_bbox_patch().set_alpha(0.8)

#takes file path as input, backslashes need to be changed to forward slashes
#i.e. "/Users/S33083/OneDrive - Noblis/Documents/EZSearchGraphs/CapellaEZSearch.csv"
def createGraph(file):
    file_name = os.path.splitext(os.path.basename(file))[0]
    raw_data = pd.read_csv(file)
    data = raw_data[:][['Contracting Agency', 'Action Obligation ($)', 'Date Signed']]

    # convert action obligation column to float
    data['Action Obligation ($)'] = data['Action Obligation ($)'].str.replace('$','', regex=True)
    data['Action Obligation ($)'] = data['Action Obligation ($)'].str.replace(',','', regex=True)
    data['Action Obligation ($)'] = data['Action Obligation ($)'].astype(float)

    # convert date signed column to int
    data['Date Signed'] = data['Date Signed'].str[-4:]
    data['Date Signed'] = data['Date Signed'].astype(int)

    if (data.size > 10) :
        data = data[(data['Date Signed']>2017)]

    mydata = data.groupby(['Date Signed', 'Contracting Agency'])['Action Obligation ($)'].sum().unstack().fillna(0)
    ax = mydata.plot(kind='bar', stacked = True)

    #plot labels
    plt.gca().ticklabel_format(axis='y', style='plain')
    plt.legend(fontsize = 9, title="Contracting Agency") 
    plt.title(file_name + ': Federal Procurement Amount by Year and Contracting Agency', fontweight='bold', fontsize=18)
    ax.set_axisbelow(True)
    plt.grid(which='major', axis='y', zorder=0)
    
    #x lables
    plt.xlabel('Year', labelpad=20, fontsize=18)
    plt.xticks(rotation=0, fontsize=15)
    
    #y labels
    plt.ylabel('Federal Procurement Amount ($)', labelpad=20, fontsize=18)
    ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
    plt.yticks(fontsize=15)

    # bars annotation
    cursor = mplcursors.cursor(hover=True)
    cursor.connect('add', show_annotation)
    
    plt.show()
        
    


# In[ ]:




