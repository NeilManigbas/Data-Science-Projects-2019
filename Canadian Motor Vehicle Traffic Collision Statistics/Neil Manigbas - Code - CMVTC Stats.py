# -*- coding: utf-8 -*-
"""
Created on Sat Jan 26 18:08:20 2019

@author: Neil
"""

### IMPORT DATA

file_dir=input('Please input your the directory where dataset is saved:')
#C:\Users\Neil\Desktop\Neil DATA SCIENTIST
import os; os.chdir(file_dir)
import pandas as pd; import numpy as np; import matplotlib.pyplot as plt

r_dataset=pd.read_csv('NCDB_2004_to_2014.csv',
                    converters={'P_SEX':str},
                    #na_values=['N','NN','NNNN'],
                    na_values=['U','UU','UUUU','N','NN','NNNN','Q','QQ','QQQQ'],
                    header=0,
                    usecols=np.r_[0,4,15:20,21], 
                    low_memory=False)


### STATISTICS

# What is the trend in terms of how many collisions reported?

y_range=range(r_dataset.C_YEAR.min(),r_dataset.C_YEAR.max()+1)
C_PER_YEAR=[]

for loop in y_range:
    C_PER_YEAR.append(len(r_dataset[r_dataset.C_YEAR==loop]))   
C_PER_YEAR=pd.Series(C_PER_YEAR, index=y_range)
C_PER_YEAR

C_2004_2009 = C_PER_YEAR.loc[2004:2009]
C_2009_2014 = C_PER_YEAR.loc[2009:2014]

line_chart1 = plt.plot(range(1,7), C_2004_2009)
line_chart2 = plt.plot(range(1,7), C_2009_2014)
plt.title('Collision Reported per Year\n5 Year Comparison')
plt.xlabel('No. of Years')
plt.ylabel('No. of Collision Reported')
plt.legend(['year 2004-2009', 'year 2009-2014'], loc=1)
plt.show()

# To answer the previous question in numbers

plt.barh(y_range,C_PER_YEAR,0.9,color='teal',edgecolor='teal')
plt.yticks(y_range, y_range)
plt.ylabel('Year', fontsize=16)
plt.xlabel('No. of Collision Reported', fontsize=16)
plt.title('Collision Reported per Year',fontsize=20)
for i, v in enumerate(C_PER_YEAR):
    plt.text(v-30000, y_range[i]+0.2, str(v))
plt.gca().invert_yaxis()
plt.show()

# How many are the actual casualties per year?

F_PER_YEAR=[]
for loop in y_range:
    F_PER_YEAR.append(len(r_dataset[(r_dataset.C_YEAR==loop)&(r_dataset.P_ISEV==3)]))
F_PER_YEAR=pd.Series(F_PER_YEAR, index=y_range)
F_PER_YEAR

F_2004_2009 = F_PER_YEAR.loc[2004:2009]
F_2009_2014 = F_PER_YEAR.loc[2009:2014]

line_chart1 = plt.plot(range(1,7), F_2004_2009)
line_chart2 = plt.plot(range(1,7), F_2009_2014)
plt.title('Fatalities Reported per Year\n5 Year Comparison')
plt.xlabel('No. of Years')
plt.ylabel('No. of Fatalities Reported')
plt.legend(['year 2004-2009', 'year 2009-2014'], loc=1)
plt.show()

# To answer the previous question in numbers

plt.bar(y_range,F_PER_YEAR,0.9,color='teal',edgecolor='teal')
plt.xticks(y_range, y_range)
plt.xlabel('Year', fontsize=16)
plt.ylabel('No. of Fatalities Reported', fontsize=16)
plt.title('Fatalities Reported per Year',fontsize=20)
for i, v in enumerate(F_PER_YEAR):
    plt.text(y_range[i]-0.2, v+0.5, str(v))
plt.show()

# Grouping Driver by Age

ag=range(0,100)
AG_DRIVER_C={'0-4'  :0,
             '5-14' :0,
             '15-19':0,
             '20-24':0,
             '25-34':0,
             '35-44':0,
             '45-54':0,
             '55-64':0,
             '65+'  :0}

for loop in ag:
    if loop in range(0,5):
        AG_DRIVER_C['0-4']+=len(r_dataset[(r_dataset.P_AGE==loop)&(r_dataset.P_USER==1)])
    elif loop in range(5,15):
        AG_DRIVER_C['5-14']+=len(r_dataset[(r_dataset.P_AGE==loop)&(r_dataset.P_USER==1)])
    elif loop in range(15,20):
        AG_DRIVER_C['15-19']+=len(r_dataset[(r_dataset.P_AGE==loop)&(r_dataset.P_USER==1)])
    elif loop in range(20,25):
        AG_DRIVER_C['20-24']+=len(r_dataset[(r_dataset.P_AGE==loop)&(r_dataset.P_USER==1)])
    elif loop in range(25,35):
        AG_DRIVER_C['25-34']+=len(r_dataset[(r_dataset.P_AGE==loop)&(r_dataset.P_USER==1)])
    elif loop in range(35,45):
        AG_DRIVER_C['35-44']+=len(r_dataset[(r_dataset.P_AGE==loop)&(r_dataset.P_USER==1)])
    elif loop in range(45,55):
        AG_DRIVER_C['45-54']+=len(r_dataset[(r_dataset.P_AGE==loop)&(r_dataset.P_USER==1)])
    elif loop in range(55,65):
        AG_DRIVER_C['55-64']+=len(r_dataset[(r_dataset.P_AGE==loop)&(r_dataset.P_USER==1)])
    else:
        AG_DRIVER_C['65+']+=len(r_dataset[(r_dataset.P_AGE==loop)&(r_dataset.P_USER==1)])

AG_DRIVER_C=pd.Series(AG_DRIVER_C, name='Collision by AG')

plt.barh(range(9),AG_DRIVER_C,0.5,color='teal',edgecolor='teal')
plt.yticks(range(9), list(AG_DRIVER_C.index.values))
plt.ylabel('Age Group', fontsize=16)
plt.xlabel('No. of Collision Reported', fontsize=16)
plt.title('Collision Reported per Year\nby Age Group',fontsize=20)
for i, v in enumerate(AG_DRIVER_C):
    plt.text(v+50, (range(9))[i]-0.125, str(v))
plt.show()

#

AG_DRIVER_F={'0-4'  :0,
             '5-14' :0,
             '15-19':0,
             '20-24':0,
             '25-34':0,
             '35-44':0,
             '45-54':0,
             '55-64':0,
             '65+'  :0}

for loop in ag:
    if loop in range(0,5):
        AG_DRIVER_F['0-4']+=len(r_dataset[(r_dataset.P_AGE==loop)&(r_dataset.P_USER==1)&(r_dataset.C_SEV==1)])
    elif loop in range(5,15):
        AG_DRIVER_F['5-14']+=len(r_dataset[(r_dataset.P_AGE==loop)&(r_dataset.P_USER==1)&(r_dataset.C_SEV==1)])
    elif loop in range(15,20):
        AG_DRIVER_F['15-19']+=len(r_dataset[(r_dataset.P_AGE==loop)&(r_dataset.P_USER==1)&(r_dataset.C_SEV==1)])
    elif loop in range(20,25):
        AG_DRIVER_F['20-24']+=len(r_dataset[(r_dataset.P_AGE==loop)&(r_dataset.P_USER==1)&(r_dataset.C_SEV==1)])
    elif loop in range(25,35):
        AG_DRIVER_F['25-34']+=len(r_dataset[(r_dataset.P_AGE==loop)&(r_dataset.P_USER==1)&(r_dataset.C_SEV==1)])
    elif loop in range(35,45):
        AG_DRIVER_F['35-44']+=len(r_dataset[(r_dataset.P_AGE==loop)&(r_dataset.P_USER==1)&(r_dataset.C_SEV==1)])
    elif loop in range(45,55):
        AG_DRIVER_F['45-54']+=len(r_dataset[(r_dataset.P_AGE==loop)&(r_dataset.P_USER==1)&(r_dataset.C_SEV==1)])
    elif loop in range(55,65):
        AG_DRIVER_F['55-64']+=len(r_dataset[(r_dataset.P_AGE==loop)&(r_dataset.P_USER==1)&(r_dataset.C_SEV==1)])
    else:
        AG_DRIVER_F['65+']+=len(r_dataset[(r_dataset.P_AGE==loop)&(r_dataset.P_USER==1)&(r_dataset.C_SEV==1)])
        
AG_DRIVER_F=pd.Series(AG_DRIVER_F, name='Fatalities by AG')

plt.barh(range(9),AG_DRIVER_F,0.5,color='orange',edgecolor='orange')
plt.yticks(range(9), list(AG_DRIVER_F.index.values))
plt.ylabel('Age Group', fontsize=16)
plt.xlabel('No. of Fatalities Reported', fontsize=16)
plt.title('Fatalities Reported per Year\nby Age Group',fontsize=20)
for i, v in enumerate(AG_DRIVER_F):
    plt.text(v+50, (range(9))[i]-0.125, str(v))
plt.show()

#

AG_DRIVER_XF={'0-4' :0,
             '5-14' :0,
             '15-19':0,
             '20-24':0,
             '25-34':0,
             '35-44':0,
             '45-54':0,
             '55-64':0,
             '65+'  :0}

for loop in ag:
    if loop in range(0,5):
        AG_DRIVER_XF['0-4']+=len(r_dataset[(r_dataset.P_AGE==loop)&(r_dataset.P_USER==1)&(r_dataset.P_ISEV==3)])
    elif loop in range(5,15):
        AG_DRIVER_XF['5-14']+=len(r_dataset[(r_dataset.P_AGE==loop)&(r_dataset.P_USER==1)&(r_dataset.P_ISEV==3)])
    elif loop in range(15,20):
        AG_DRIVER_XF['15-19']+=len(r_dataset[(r_dataset.P_AGE==loop)&(r_dataset.P_USER==1)&(r_dataset.P_ISEV==3)])
    elif loop in range(20,25):
        AG_DRIVER_XF['20-24']+=len(r_dataset[(r_dataset.P_AGE==loop)&(r_dataset.P_USER==1)&(r_dataset.P_ISEV==3)])
    elif loop in range(25,35):
        AG_DRIVER_XF['25-34']+=len(r_dataset[(r_dataset.P_AGE==loop)&(r_dataset.P_USER==1)&(r_dataset.P_ISEV==3)])
    elif loop in range(35,45):
        AG_DRIVER_XF['35-44']+=len(r_dataset[(r_dataset.P_AGE==loop)&(r_dataset.P_USER==1)&(r_dataset.P_ISEV==3)])
    elif loop in range(45,55):
        AG_DRIVER_XF['45-54']+=len(r_dataset[(r_dataset.P_AGE==loop)&(r_dataset.P_USER==1)&(r_dataset.P_ISEV==3)])
    elif loop in range(55,65):
        AG_DRIVER_XF['55-64']+=len(r_dataset[(r_dataset.P_AGE==loop)&(r_dataset.P_USER==1)&(r_dataset.P_ISEV==3)])
    else:
        AG_DRIVER_XF['65+']+=len(r_dataset[(r_dataset.P_AGE==loop)&(r_dataset.P_USER==1)&(r_dataset.P_ISEV==3)])
        
AG_DRIVER_XF=pd.Series(AG_DRIVER_XF, name='Driver: F by AG')

plt.barh(range(9),AG_DRIVER_F,0.5,color='orange',edgecolor='orange')
plt.barh(range(9),AG_DRIVER_XF,0.5,color='blue',edgecolor='blue')
plt.yticks(range(9), list(AG_DRIVER_XF.index.values))
plt.ylabel('Age Group', fontsize=16)
plt.xlabel('No. of Fatalities Reported', fontsize=16)
plt.title('Driver: Fatalities - Fatalities Reported per Year\nby Age Group',fontsize=20)
for i, (v1, v2) in enumerate(zip(AG_DRIVER_XF, AG_DRIVER_F)):
    try:
        plt.text(v1+10, (range(9))[i]-0.125, str(v1)+'-'+str('%.1f' % (v1/v2*100))+'%')
    except ZeroDivisionError:
        pass
plt.show()

# Driver by Gender
gen=list(r_dataset.P_SEX.unique())
del gen[gen.index('N')]
gen
G_DRIVER_C=[]
G_DRIVER_F=[]

for loop in gen:
    G_DRIVER_F.append(len(r_dataset[(r_dataset.P_SEX==loop)&(r_dataset.P_USER==1)&(r_dataset.C_SEV==1)]))
    G_DRIVER_C.append(len(r_dataset[(r_dataset.P_SEX==loop)&(r_dataset.P_USER==1)]))

G_DRIVER_C=pd.Series(G_DRIVER_C, index=gen, name='Collision')
G_DRIVER_C
G_DRIVER_F=pd.Series(G_DRIVER_F, index=gen, name='Fatalities')
G_DRIVER_F

#

c = ['pink', 'green', 'gray']
l = ['Female', 'Male', 'Not Sure']
e = (0, 0, 0.3)
plt.pie(G_DRIVER_C, colors=c, labels=G_DRIVER_C ,explode=e,autopct='%0.1f%%', counterclock=True, shadow=False)
plt.title('Driver:Collision Report\nby Gender')
plt.legend(l,loc=4)
plt.show()

#

c = ['pink', 'green', 'gray']
l = ['Female', 'Male', 'Not Sure']
e = (0, 0, 0.3)
plt.pie(G_DRIVER_F, colors=c, labels=G_DRIVER_F ,explode=e,autopct='%0.1f%%', counterclock=True, shadow=False)
plt.title('Driver:Fatality Report\nby Gender')
plt.legend(l,loc=4)
plt.show()

#

G_DRIVER_PCT=pd.concat([G_DRIVER_C,G_DRIVER_F], axis=1)
G_DRIVER_PCT['Pct F/C']=((G_DRIVER_PCT['Fatalities'].astype(float))
                                /(G_DRIVER_PCT['Collision'].astype(float))
                                *100).round(2)
G_DRIVER_PCT

#

G_DRIVER_FAT=[]

for loop in gen:
    G_DRIVER_FAT.append(len(r_dataset[(r_dataset.P_SEX==loop)&(r_dataset.P_USER==1)&(r_dataset.P_ISEV==3)]))
G_DRIVER_FAT=pd.Series(G_DRIVER_FAT, index=gen, name='Driver F')
G_DRIVER_FAT

G_DRIVER_PCT=pd.concat([G_DRIVER_PCT,G_DRIVER_FAT], axis=1)
G_DRIVER_PCT['Pct DF/F']=((G_DRIVER_PCT['Driver F'].astype(float))
                                /(G_DRIVER_PCT['Fatalities'].astype(float))
                                *100).round(2)
G_DRIVER_PCT

