# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 21:48:56 2018

@author: soug9
"""


import pandas as pd
import numpy as np
import re
import datetime
import pickle

## load data ##

# 고객정보
customer = pd.read_table(r'C:\Users\soug9\Desktop\Shcard Summer School\data\01_고객정보.txt',
                         sep=';',  engine='python')

# 승인정보
transaction = pd.read_table(r'C:\Users\soug9\Desktop\Shcard Summer School\data\02_승인정보.txt',
                         sep=';',  engine='python')

# 가맹점정보
#store = pd.read_table(r'C:\Users\soug9\Desktop\Shcard Summer School\data\03_가맹점정보.txt', sep=';',  engine='python')

f=open(r'C:\Users\soug9\Desktop\Shcard Summer School\data\03_가맹점정보.txt','r')

s=[]
for line in f:
    s.append(line.strip())

for i in range(len(s)) :
    s[i] = s[i].split(';')

store = pd.DataFrame.from_records(s[1:])    
store.columns = s[0]

# 온라인유료콘텐츠
online = pd.read_table(r'C:\Users\soug9\Desktop\Shcard Summer School\data\04_온라인유료콘텐츠.txt',
                         sep=';',  engine='python')

# 이용금액 코드표
use_amt = pd.read_table(r'C:\Users\soug9\Desktop\Shcard Summer School\data\이용금액 코드표.txt',
                         sep='\t',  engine='python')


## preprocessing ##

# 이용금액 코드표
# create derived variable - AMT -> AMT1
use_amt['AMT1'] = use_amt['AMT']
use_amt['AMT1'] = use_amt['AMT1'].apply(lambda x : re.sub('천원이하','000',x))
use_amt['AMT1'] = use_amt['AMT1'].apply(lambda x : re.sub('만원이하','0000',x))
use_amt['AMT1'] = use_amt['AMT1'].apply(lambda x : re.sub('만원초과','0001',x))
use_amt['AMT1'] = use_amt['AMT1'].astype('int')

# 승인정보, 온라인유료콘텐츠
# create derived variable - APV_TS_D + TIME => DATETIME 
def toDatetime(df) : 
    # APV_TS_D + TIME = create new feature named 'DATETIME' whose type is datetime
    df['APV_TS_D'] = df['APV_TS_D'].astype(str)
    df['DATETIME'] = df[['APV_TS_D', 
              'TIME']].apply(lambda x : datetime.datetime(int(x.values[0][:4]),
              int(x.values[0][4:6]), int(x.values[0][6:8]),
              x.values[1]), axis=1)
    return df

transaction = toDatetime(transaction)
online = toDatetime(online)

# merge online + use_amt
online = pd.merge(online, use_amt, on='USE_AMT')
online = online.drop(['AMT', 'USE_AMT'], axis=1)

# merge transaction + use_amt
transaction = pd.merge(transaction, use_amt, on='USE_AMT')
transaction = transaction.drop(['AMT', 'USE_AMT'], axis=1)

## join - create new dataset ##

# online + customer + store
ocs = pd.merge(online, customer, how='left')
ocs = pd.merge(ocs, store, how='left')

# save to excel
ocs.to_excel(r'C:\Users\soug9\Desktop\Shcard Summer School\data\online+customer+store.xlsx')

# save to txt
with open(r'C:\Users\soug9\Desktop\Shcard Summer School\data\online+customer+store.txt',"wb") as fp :
        pickle.dump(ocs,fp)

with open(r'C:\Users\soug9\Desktop\Shcard Summer School\data\online+customer+store.txt',"rb") as fp :
        ocs_test = pickle.load(fp)   


# transaction + customer + store
tcs = pd.merge(transaction, customer, how='left')
tcs = pd.merge(tcs, store, how='left')

# save to excel
tcs.to_excel(r'C:\Users\soug9\Desktop\Shcard Summer School\data\transaction+customer+store.xlsx')

# save to txt
with open(r'C:\Users\soug9\Desktop\Shcard Summer School\data\transaction+customer+store.txt',"wb") as fp :
        pickle.dump(tcs,fp)

with open(r'C:\Users\soug9\Desktop\Shcard Summer School\data\transaction+customer+store.txt',"rb") as fp :
        tcs_test = pickle.load(fp)   



