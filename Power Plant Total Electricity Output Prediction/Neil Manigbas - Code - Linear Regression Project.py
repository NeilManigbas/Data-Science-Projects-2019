# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 16:50:37 2019

@author: Neil
"""
### IMPORTING DATASET CSV FILE

import os

datapath=str(r'C:\Users\nmanigba\Downloads\Regression')
os.chdir(datapath)

import pandas as pd

ds=pd.read_csv('PowerPlantDataSet .csv',dtype='float')
ds.reset_index()

### EXAMINING DATASET

ds.shape  # (9568, 5)
ds.info()
ds.isnull().values.any()
desc=ds.describe()
ds.columns

## Checking Normal Distribution

import seaborn as sbn

sbn.boxplot(data=ds)
ds.columns
sbn.distplot(ds.AT)
sbn.distplot(ds.V)
sbn.distplot(ds.AP)
sbn.distplot(ds.RH)
sbn.distplot(ds.PE)

## Checking Correlation

sbn.pairplot(ds)

corr=ds.corr()
sbn.heatmap(corr, cmap="YlGnBu", xticklabels=ds.columns, yticklabels=ds.columns)

### SPLITTING, FITTING AND TRAINING

## Importing packages

import sklearn as sk
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression

import statsmodels.api as sm

## Train-Test data split

from sklearn.model_selection import train_test_split

x = ds.iloc[:,0:4]
y = ds.iloc[:,4]
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=.2,random_state=None)

print(x_train.shape,y_train.shape)
print(x_test.shape,y_test.shape)

## Model Fitting

regr = LinearRegression()

model=regr.fit(x_train, y_train)

## Model Checking

y_pred = regr.predict(x_test)

import matplotlib.pyplot as plt

plt.scatter(y_test,y_pred)
plt.xlabel('True Values')
plt.ylabel('Prediction')

## SUMMARY of Scores

score = sk.metrics.r2_score(y_test, y_pred)
skscoring=sorted(sk.metrics.SCORERS.keys())
r2=cross_val_score(regr,x_train,y_train,cv=5,scoring='r2')

n=len(x_train)
p=len(x_train.columns)
adjR2 = 1-(1-r2)*(n-1)/(n-p-1) #adjusted R^2 formula

negMSE=cross_val_score(regr,x_train,y_train,cv=5,scoring='neg_mean_squared_error')

import numpy as np
RMSE=list(np.sqrt(-(negMSE)))


### SPLITTING, FITTING, TRAINING AND SUMMARY with OLS function

import statsmodels.api as sm
from sklearn.model_selection import KFold

ds_summ={}
n_kfold=5
kf = KFold(n_splits = n_kfold, shuffle = True, random_state = None)
ds_i=iter(kf.split(ds))
for loop in range(0,n_kfold):
    ds_set=next(ds_i)
    x_train = ds.iloc[ds_set[0],0:4]
    x_train = sm.add_constant(x_train)
    y_train = ds.iloc[ds_set[0],4]
    
    x_test = ds.iloc[ds_set[1],0:4]
    x_test = sm.add_constant(x_test)
    y_test = ds.iloc[ds_set[1],4]
    
    model=sm.OLS(y_train,x_train).fit()
    y_pred=model.predict(x_test)
    
    ds_summ[loop]=model.summary()

ds_summ[4]

import seaborn as sbn
import matplotlib.pyplot as plt

sbn.scatterplot(x=y_test,y=y_pred)
plt.xlabel('True Values')
plt.ylabel('Prediction')

