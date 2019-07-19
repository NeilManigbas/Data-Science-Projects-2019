# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 16:16:39 2019

@author: nmanigba
"""

import pandas as pd
import os

### IMPORT TXT FILE DATASET

datapath=str(r'C:\Users\nmanigba\Desktop\Data Mining Project - Neil Manigbas\Classification')
os.chdir(datapath)
df=pd.read_csv('occupancy_data.txt')
df.reset_index(inplace=False)
#df.drop(columns='index',inplace=True)

### UNDERSTANDING THE DATA

df.shape
df.info()
desc=df.describe()

import seaborn as sbn

sbn.boxplot(data=df)

df.columns
df.iloc[:,0].values.dtype
df=df.drop(columns=['date']) #str

df.isnull().values.any()

sbn.boxplot(data=df.drop(columns=['date'],axis=1))

df.columns
sbn.distplot(df.Temperature)
sbn.distplot(df.Humidity)
sbn.distplot(df.Light)
sbn.distplot(df.CO2)
sbn.distplot(df.Occupancy)

## Correlation Matrix

corr=df.corr()
sbn.heatmap(corr, cmap="YlGnBu", xticklabels=df.columns, yticklabels=df.columns)

### DATA CLEANING
## Dealing with the significant Outliers

from scipy import stats
import numpy as np

z = np.abs(stats.zscore(df))
len((np.where(z > 3))[0]) # 346
df = df[(z < 3).all(axis=1)]

### DATA MODELING

## Importing classifier library

from sklearn.tree import DecisionTreeClassifier

## Assigning the classifier

classifier=DecisionTreeClassifier()

## Importing other libraries

import statsmodels.api as sm
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score, confusion_matrix

## K-Fold split, train, test and score

cm={}
acc=[]
n_kfold=5
kf = KFold(n_splits = n_kfold, shuffle = True, random_state = None)
df_i=iter(kf.split(df))
for loop in range(n_kfold):
    df_set=next(df_i)
    x_train = df.iloc[df_set[0],0:6]
    y_train = df.iloc[df_set[0],6]
    
    x_test = df.iloc[df_set[1],0:6]
    y_test = df.iloc[df_set[1],6]
    
    classifier.fit(x_train,y_train)
    
    y_pred = classifier.predict(x_test)
    
    acc.append(accuracy_score(y_pred,y_test))
    cm[loop]=confusion_matrix(y_test,y_pred)

## Validating prediction model
    
np.mean(acc)
cm[0]
cm[1]
cm[2]
cm[3]
cm[4]

import seaborn as sbn
import matplotlib.pyplot as plt

sbn.scatterplot(y_test,y_pred)
plt.xlabel('True Values')
plt.ylabel('Prediction')
