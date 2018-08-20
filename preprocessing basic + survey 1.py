# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 16:19:59 2018

@author: soug9
"""

import pandas as pd
import numpy as np
import pickle

## load data - survey ##

survey = pd.read_table(r'C:\Users\soug9\Desktop\Shcard Summer School\data\서베이결과.txt',
                         sep=';',  engine='python')

survey.columns

col = ['CLNN', 'SEX_CCD', 'Q17_1', 'Q17_2',
       'Q17_3', 'Q17_4', 'Q17_5', 'Q17_6', 'Q17_7', 'Q17_8', 'Q17_9', 'Q17_10',
       'Q18', 'Q19', 'Q20', 'Q21', 'Q22', 'Q23', 'Q24', 'Q25_1', 'Q25_2',
       'Q25_3', 'Q25_4', 'Q25_5', 'Q26', 'Q27']

survey = survey[col]


## create derived variable - Q17_1 ~ Q17_10 => Q17(횟수) ##

survey17 = survey[['Q17_1', 'Q17_2',
       'Q17_3', 'Q17_4', 'Q17_5', 'Q17_6', 'Q17_7', 'Q17_8', 'Q17_9', 'Q17_10']]

survey['Q17'] = [survey17.iloc[i].notnull().sum() for i in range(len(survey17))]

survey = survey.drop(['Q17_1', 'Q17_2','Q17_3', 'Q17_4', 'Q17_5', 'Q17_6', 'Q17_7', 'Q17_8', 'Q17_9', 'Q17_10'], axis=1)


## create derived variable - Q17 => zipdol (0-밖돌, 1-중간집돌, 2-집돌) ##
        
survey['zipdol'] = [0]*len(survey)

survey['zipdol'][survey['Q17']>=8] = 2
survey['zipdol'][(survey['Q17']<8) & (survey['Q17']>3)] = 1

# save to excel
survey.to_excel(r'C:\Users\soug9\Desktop\Shcard Summer School\data\survey17-27+zipdol.xlsx')

# save to txt
with open(r'C:\Users\soug9\Desktop\Shcard Summer School\data\survey17-27+zipdol.txt',"wb") as fp :
        pickle.dump(survey,fp)

with open(r'C:\Users\soug9\Desktop\Shcard Summer School\data\survey17-27+zipdol.txt',"rb") as fp :
        survey17_27_zipdol = pickle.load(fp)   


## join - create new dataset ##

# online + customer + store + survey17_27_zipdol
        
# load data
with open(r'C:\Users\soug9\Desktop\Shcard Summer School\data\online+customer+store.txt',"rb") as fp :
        ocs = pickle.load(fp)         

# merge
survey = survey.drop(['SEX_CCD'],axis=1)
ocss = pd.merge(ocs, survey, on='CLNN')

# save to excel
ocss.to_excel(r'C:\Users\soug9\Desktop\Shcard Summer School\data\online+customer+store+survey.xlsx')

# save to txt
with open(r'C:\Users\soug9\Desktop\Shcard Summer School\data\online+customer+store+survey.txt',"wb") as fp :
        pickle.dump(ocss,fp)

with open(r'C:\Users\soug9\Desktop\Shcard Summer School\data\online+customer+store+survey.txt',"rb") as fp :
        ocss_test = pickle.load(fp)   




