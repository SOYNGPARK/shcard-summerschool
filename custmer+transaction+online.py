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

# load data

# 고객정보
customer = pd.read_table(r'C:\Users\soug9\Desktop\Shcard Summer School\data\01_고객정보.txt',
                         sep=';',  engine='python')

# 승인정보
transaction = pd.read_table(r'C:\Users\soug9\Desktop\Shcard Summer School\data\02_승인정보.txt',
                         sep=';',  engine='python')

# 가맹점정보
#store = pd.read_table(r'C:\Users\soug9\Desktop\Shcard Summer School\data\03_가맹점정보.txt', sep=';',  engine='python')

f=open(r'C:\Users\soug9\Desktop\Shcard Summer School\data\03_가맹점정보.txt','r')

trans=[]
for line in f:
    trans.append(line.strip())

for i in range(len(trans)) :
    trans[i] = trans[i].split(';')

store = pd.DataFrame.from_records(trans[1:])    
store.columns = trans[0]

# 온라인유료콘텐츠
online = pd.read_table(r'C:\Users\soug9\Desktop\Shcard Summer School\data\04_온라인유료콘텐츠.txt',
                         sep=';',  engine='python')

# 이용금액 코드표
use_amt = pd.read_table(r'C:\Users\soug9\Desktop\Shcard Summer School\data\이용금액 코드표.txt',
                         sep='\t',  engine='python')


# deal with use_amt
use_amt['AMT1'] = use_amt['AMT']
use_amt['AMT1'] = use_amt['AMT1'].apply(lambda x : re.sub('천원이하','000',x))
use_amt['AMT1'] = use_amt['AMT1'].apply(lambda x : re.sub('만원이하','0000',x))
use_amt['AMT1'] = use_amt['AMT1'].apply(lambda x : re.sub('만원초과','0001',x))
use_amt['AMT1'] = use_amt['AMT1'].astype('int')


# merge custmer+transaction+online
online = pd.merge(online, use_amt, on='USE_AMT')
transaction = pd.merge(transaction, use_amt, on='USE_AMT')

online_new = pd.merge(online[['CLNN', 'APV_TS_D', 'TIME', 'MCT_N', 'AMT1']], customer, how='left')
online_new = pd.merge(online_new, store, how='left')


# create derived variable - APV_TS_D + TIME => DATETIME 
online_new['APV_TS_D'].value_counts().sort_index()
online_new['TIME'].value_counts()

# APV_TS_D + TIME = create new feature named 'DATETIME' whose type is datetime
online_new['APV_TS_D'] = online_new['APV_TS_D'].astype(str)

online_new['DATETIME'] = online_new[['APV_TS_D', 
          'TIME']].apply(lambda x : datetime.datetime(int(x.values[0][:4]),
          int(x.values[0][4:6]), int(x.values[0][6:8]),
          x.values[1]), axis=1)


# save to excel
online_new.to_excel(r'C:\Users\soug9\Desktop\Shcard Summer School\data\custmer+transaction+online.xlsx')

# save to txt
with open(r'C:\Users\soug9\Desktop\Shcard Summer School\data\custmer+transaction+online.txt',"wb") as fp :
        pickle.dump(online_new,fp)

with open(r'C:\Users\soug9\Desktop\Shcard Summer School\data\custmer+transaction+online.txt',"rb") as fp :
        online_new_test = pickle.load(fp)   




