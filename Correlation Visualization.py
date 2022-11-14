#!/usr/bin/env python
# coding: utf-8

"""

This algorithm aims to visualize correlation using the following methods:
    
    - Scatter Matrix
    - Heatmap
    - Network Graph

"""

#Importer Modules
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as data
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import networkx as nx
import warnings
warnings.filterwarnings("ignore")
from pandas.plotting import scatter_matrix


start_time = datetime.datetime.now() - datetime.timedelta(days= 1*65)
end_time = datetime.datetime.now().date().isoformat()  

index_dow = ['CAT','CHTR','CL','CMCSA','COF','COP','COST','CRM','CSCO','CVS','CVX','DD','DHR','DIS','DOW','DUK','EMR','EXC','F','FDX','GD','GE','GILD','GM','GOOG','GOOGL']
#index_dow = ['AAPL','AMZN','TSLA','CSCO','F','GOOG','JPM']
             
index = data.DataReader(index_dow, start_time, end_time)

indicepanel = index['Adj Close']
indicepanel = indicepanel.fillna(method='ffill')
indicepanel = indicepanel.dropna()

## Part 1: classical visualization
# Create scatter matrix one correlation
plt.scatter(indicepanel['CAT'], indicepanel['COST']) #Create scatter matrix multi correlation

sm = scatter_matrix(indicepanel, figsize = (15, 15)) #Create Heatmap

corr = indicepanel.corr()
fig, ax = plt.subplots(figsize=(15, 15))
colormap = sns.diverging_palette(220, 10, as_cmap=True)
sns.heatmap(corr, cmap=colormap, annot=True, fmt=".2f")
plt.xticks(range(len(corr.columns)), corr.columns);
plt.yticks(range(len(corr.columns)), corr.columns)
plt.show()

## Part 2: Create network graph
#Create Adjacency Matrix
lenliste = len(indicepanel.columns)
matrix = []

for n in range (lenliste):
    liste = []
    
    for i in range (lenliste):
        
        if n != i:
            r = np.corrcoef(indicepanel.iloc[:,n], indicepanel.iloc[:,i])
    
            if r[0, 1] > 0.75:
                num = 1
            else:
                num = 0
        else:
            num = 0   

        liste.append(num)
        
    matrix.append(liste)



matrixdf = pd.DataFrame(matrix)
matrixdf.columns = indicepanel.columns
matrixdfn = matrixdf.set_index(indicepanel.columns)

#Create Network Graph
G = nx.from_numpy_matrix(np.array(matrixdfn), create_using=nx.MultiDiGraph())
headers = matrixdfn.columns

def make_label_dict(labels):
    l = {}
    for i, label in enumerate(labels):
        l[i] = label
    return l

labels=make_label_dict(headers)
pos = nx.spring_layout(G, k=1.5)
plt.figure(figsize=(15,15))
nx.draw(G,pos,node_size=1000, labels=labels)
nx.draw_networkx_edges(G, pos)
plt.show()

