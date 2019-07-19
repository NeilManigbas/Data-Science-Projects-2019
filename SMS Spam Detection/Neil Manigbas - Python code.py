# # # # ----- Python Project ----- # # #
# # # # --- by Neil Manigbas --- # # #

# # Data Exploration

# Import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Suppress warning errors
import warnings
warnings.simplefilter(action='ignore')

# Change directory where data files are located
import os
os.chdir(r'C:\Users\nmanigba\Desktop\Neil Manigbas - Python Project\Data')

# Read files:
train = pd.read_csv("Store_Train_Forecast_Class.csv")
test = pd.read_csv("Store_Test_Forecast_Class.csv")

train['dataset']='train'
test['dataset']='test'

# Combining train and test datasets, ignoring index
data = pd.concat([train, test], ignore_index=True)
print (train.shape, test.shape, data.shape)

# Statistics
print(data.describe())

# Null values count
print(data.apply(lambda x: sum(x.isnull())))

# Unique values count
print('\nUnique values')
print(data.apply(lambda x: len(x.unique())))

# Filter categorical variables
categorical_columns = [x for x in data.dtypes.index if data.dtypes[x]=='object']
# Exclude ID cols and source:
categorical_columns = [x for x in categorical_columns if x not in ['Item_Identifier','Outlet_Identifier','dataset']]
# Print frequency of categories
for col in categorical_columns:
    print ('\nFrequency of Categories for varible %s'%col)
    print (data[col].value_counts())

#Checking Outliers
print(data.describe())

import seaborn as sbn

graph=sbn.boxplot(data=data[data.columns[data.dtypes!='object']])
graph.set_xticklabels(graph.get_xticklabels(),rotation=90)
plt.title('Outliers - Unscaled',fontsize=18)
plt.show()

from sklearn.preprocessing import StandardScaler
sc=StandardScaler()
data_scaled=sc.fit_transform(np.nan_to_num(data[data.columns[data.dtypes!='object']].astype(float)))

graph=sbn.boxplot(data=data_scaled)
plt.xticks(list(range(0,len(data.columns[data.dtypes!='object']))),data[data.columns[data.dtypes!='object']].columns)
graph.set_xticklabels(graph.get_xticklabels(),rotation=90)
plt.title('Outliers - Scaled',fontsize=18)
plt.show()

# Dealing with the Outliers
from scipy import stats

z = np.abs(stats.zscore(data[data.columns[data.dtypes!='object']]))
print(len((np.where(z > 3))[0]),'outliers out of',len(data))    
print('%.2f'% (len((np.where(z > 3))[0])/len(data)*100),'% of the dataset')


# # Data Cleaning

# IMPUTING Item_Weight variable

# Determine the average weight per item
item_avg_weight = data.pivot_table(values='Item_Weight', index='Item_Identifier')
print ('Average weight for each item:')
print (item_avg_weight.head(10))

# Get a boolean variable specifying missing Item_Weight values
miss_bool = data['Item_Weight'].isnull() 

# Impute data and check missing values count before and after imputation to confirm
print ('\nNull value count before imputing: %d'% sum(miss_bool))
data.loc[miss_bool,'Item_Weight'] = data.loc[miss_bool,'Item_Identifier'].apply(lambda x: item_avg_weight.loc[x])
print ('Count after imputing: %d'% sum(data['Item_Weight'].isnull()))

# IMPUTE Outlet_Size variable

# Import mode function
from scipy.stats import mode

# Determing the Outlet_Size mode for each Outlet_Type
outlet_size_mode = data.dropna().pivot_table(values='Outlet_Size', columns='Outlet_Type',aggfunc=(lambda x: mode(x).mode[0]))
print ('Mode for each Outlet_Type:')
print (outlet_size_mode)

# Get a boolean variable specifying missing Item_Weight values
miss_bool = data['Outlet_Size'].isnull() 

# Impute data and check missing values count before and after imputation to confirm
print ('\nNull value count before imputing: %d'% sum(miss_bool))
data.loc[miss_bool,'Outlet_Size'] = data.loc[miss_bool,'Outlet_Type'].apply(lambda x: outlet_size_mode[x])
print ('Count after imputing:',sum(data['Outlet_Size'].isnull()))


# # Feature Engineering

# Modify Item_Visibility
# Found the minimum value is 0
# Consider it as missing information and impute it with mean visibility of that product

# Determine average visibility of a product
visibility_avg = data.pivot_table(values='Item_Visibility', index='Item_Identifier')

#Impute 0 values with mean visibility of that product:
miss_bool = (data['Item_Visibility'] == 0)

print ('Number of 0 values before imputing: %d'%sum(miss_bool))
data.loc[miss_bool,'Item_Visibility'] = data.loc[miss_bool,'Item_Identifier'].apply(lambda x: visibility_avg.loc[x])
print ('Count after imputing: %d'%sum(data['Item_Visibility'] == 0))

# Classify type of item

# Get the first two characters of ID
data['Item_Type_Combined'] = data['Item_Identifier'].apply(lambda x: x[0:2])
# Rename them to more intuitive categories
data['Item_Type_Combined'] = data['Item_Type_Combined'].map({'FD':'Food',
                                                             'NC':'Non-Consumable',
                                                             'DR':'Drinks'})
# Drop the column which have been converted
data.drop(['Item_Type'],axis=1,inplace=True)

print(data['Item_Type_Combined'].value_counts())

# Determine the years of operation of a store
data['Outlet_Years'] = 2013 - data['Outlet_Establishment_Year']

# Drop the column which have been converted
data.drop(['Outlet_Establishment_Year'],axis=1,inplace=True)

print(data['Outlet_Years'].describe())

# Modify categories of Item_Fat_Content

# Change categories of low fat
print ('Original Categories:')
print (data['Item_Fat_Content'].value_counts())

print ('\nModified Categories:')
data['Item_Fat_Content'] = data['Item_Fat_Content'].replace({'LF':'Low Fat',
                                                             'reg':'Regular',
                                                             'low fat':'Low Fat'})


# Mark non-consumables as separate category
data.loc[data['Item_Type_Combined']=='Non-Consumable','Item_Fat_Content'] = 'Non-Edible'
print ('\nModified Categories(v2):')
print(data['Item_Fat_Content'].value_counts())

# Numerical and One-Hot Coding of Categorical variables

# Import library
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()

# New variable for Outlet_Identifier
data['Outlet'] = le.fit_transform(data['Outlet_Identifier'])
var_mod = ['Item_Fat_Content','Outlet_Location_Type','Outlet_Size','Item_Type_Combined','Outlet_Type','Outlet']
le = LabelEncoder()
for i in var_mod:
    data[i] = le.fit_transform(data[i])

# Exporting Data

# Divide into test and train
train = data.loc[data['dataset']=='train']
test = data.loc[data['dataset']=='test']

# Drop unnecessary columns
test.drop(['Item_Outlet_Sales','dataset'],axis=1,inplace=True)
train.drop(['dataset'],axis=1,inplace=True)

# Define target and ID columns
IDcol = ['Item_Identifier','Outlet_Identifier']
target = 'Item_Outlet_Sales'
predictors = [x for x in train.columns if x not in [target]+IDcol]

# Correlation heat map - part of data exploration
import seaborn as sbn

dcorr=train.corr()
mask = np.zeros_like(dcorr)
mask[np.triu_indices_from(mask)] = True
with sbn.axes_style("white"):
    ax = sbn.heatmap(dcorr, mask=mask, cmap="YlGnBu")
plt.show()

sbn.pairplot(train)


# # Model Building

# Importing packages
from sklearn.model_selection import GridSearchCV
import datetime as dt

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import AdaBoostRegressor, RandomForestRegressor

# Perform GridSearch

# Assuming parameters
best_params =   {
        'LR':       [LinearRegression(),
                     {'normalize':['True','False']}],
        'Ridge':    [Ridge(),
                     {'alpha':[0.25,0.5,0.75],
                      'normalize':['True','False']}],
        'KNN':      [KNeighborsRegressor(),
                     {'n_neighbors':list(range(5,9)),
                      'weights':['uniform','distance']}],
        'adaboost': [AdaBoostRegressor(),
                     {'n_estimators':[50,60,70,80]}],
        'DT':       [DecisionTreeRegressor(),
                     {'max_depth':[None,5,10,15],
                      'min_samples_leaf':[100,150,200]}],
        'RF':       [RandomForestRegressor(),
                     {'n_estimators':[70,80,90,100],
                      'max_depth':[None,2,4,6,8],
                      'min_samples_leaf':[100,200,300],
                      'n_jobs':[2,3,4]}]
                }

# Performing Gridsearch
for i in best_params.keys():
    print(i+' '+'started...')
    strtime=dt.datetime.now()
    model=GridSearchCV(best_params[i][0],best_params[i][1],cv=5)
    model.fit(train[predictors],train[target])
    best_params[i]=model.best_params_
    end_sec=(dt.datetime.now()-strtime).total_seconds()
    print('...'+'DONE ('+str(end_sec)+' seconds)\n')

# Print best parameters by Gridsearch
print(best_params)

# Create a function to return prediction scores
from sklearn import metrics
from sklearn.model_selection import cross_val_score
import re

def cv_score(alg, dtrain, dtest, predictors, target):
    # Fit the algorithm on the data
    alg.fit(dtrain[predictors], dtrain[target])
        
    #Predict training set:
    dtrain[(re.split('\(', str(alg), 1))[0]] = alg.predict(dtrain[predictors])
    
    # Perform cross-validation
    n=len(data)
    p=len(data[predictors].columns)
    cv_r2 = cross_val_score(alg, dtrain[predictors], dtrain[target], cv=20, scoring='r2')
    cv_r2adj = (1-(1-cv_r2))*(n-1)/(n-p-1)
    cv_RMSE = cross_val_score(alg, dtrain[predictors], dtrain[target], cv=20, scoring='neg_mean_squared_error')
    cv_RMSE = np.sqrt(np.abs(cv_RMSE))
    
    # Print model report
    r2={'mean':np.mean(cv_r2),'std':np.std(cv_r2),'min':np.min(cv_r2),'max':np.max(cv_r2)}
    r2adj={'mean':np.mean(cv_r2adj),'std':np.std(cv_r2adj),'min':np.min(cv_r2adj),'max':np.max(cv_r2adj)}
    RMSE={'mean':np.mean(cv_RMSE),'std':np.std(cv_RMSE),'min':np.min(cv_RMSE),'max':np.max(cv_RMSE)}
    model_report=pd.DataFrame([r2,r2adj,RMSE], index=['R^2','Adjusted R^2','RMSE'], columns=['mean','std','min','max'])
    print ('\nModel Report')
    print ('Algorithm : '+(re.split('\(', str(alg), 1))[0])
    print (model_report.round(4))

    # Predict on testing data
    dtest[(re.split('\(', str(alg), 1))[0]] = alg.predict(dtest[predictors])

# a) Linear Regression
alg_LR = LinearRegression(normalize=True)
cv_score(alg_LR, train, test, predictors, target)
coef_LR = pd.Series(alg_LR.coef_, predictors).sort_values()
coef_LR.plot(kind='bar', title='Model Coefficients')
plt.show()

# b) Ridge regression
alg_Ridge = Ridge(alpha=0.25,normalize='True')
cv_score(alg_Ridge, train, test, predictors, target)
coef_Ridge = pd.Series(alg_Ridge.coef_, predictors).sort_values()
coef_Ridge.plot(kind='bar', title='Model Coefficients')
plt.show()

# c) K-Nearest Neighbours
alg_KNN = KNeighborsRegressor(n_neighbors=8,weights='distance')
cv_score(alg_KNN, train, test, predictors, target)

# d) Adaboost
alg_adaboost = AdaBoostRegressor(n_estimators=50)
cv_score(alg_adaboost, train, test, predictors, target)

# e) Decision Tree
alg_DT = DecisionTreeRegressor(max_depth=5,min_samples_leaf=100)
cv_score(alg_DT, train, test, predictors, target)
coef_DT = pd.Series(alg_DT.feature_importances_, predictors).sort_values(ascending=False)
coef_DT.plot(kind='bar', title='Feature Importances')
plt.show()

# f) Random Forest
alg_RF = RandomForestRegressor(max_depth=None,min_samples_leaf=100,n_estimators=100,n_jobs=4)
cv_score(alg_RF, train, test, predictors, target)
coef_RF = pd.Series(alg_RF.feature_importances_, predictors).sort_values(ascending=False)
coef_RF.plot(kind='bar', title='Feature Importances')
plt.show()


