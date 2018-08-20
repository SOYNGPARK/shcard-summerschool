# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 18:14:17 2018

@author: soug9
"""

import pickle
import numpy as np
import pandas as pd
 

## 설문조사 결과 온라인콘텐츠를 이용해 본 회원 ##
#동영상 스트리밍 20, 21, 22, 23 중 하나라도 1번 한 응답자 제거
#웹툰 26, 27 중 하나라도 1번 한 응답자 제거
#유료 어플 25 1번 한 응답자 제거

with open(r'C:\Users\soug9\Desktop\Shcard Summer School\data\survey17-27+zipdol.txt',"rb") as fp :
        survey17_27 = pickle.load(fp)  

survey17_27.columns

video = survey17_27['CLNN'][(survey17_27['Q20'] != 1) & (survey17_27['Q21'] != 1) & (survey17_27['Q22'] != 1) & (survey17_27['Q23'] != '1')]
video = video.tolist()

webtoon = survey17_27['CLNN'][(survey17_27['Q26'] != 1) & (survey17_27['Q27'] != '1')]
webtoon = webtoon.tolist()

app = survey17_27['CLNN'][survey17_27['Q25_1'] != 1]
app = app.tolist()

total = video + webtoon + app
total = list(set(total))

survey17_27_online = survey17_27[survey17_27['CLNN'].isin(total)]

# save to excel
survey17_27_online.to_excel(r'C:\Users\soug9\Desktop\Shcard Summer School\data\survey17-27+zipdol_online.xlsx')

## join - create new dataset ##
## 설문조사 결과 온라인콘텐츠를 이용해 본 회원 중 온라인(online)/오프라인(transaction) 결제 내역이 있는 회원##

# load data
with open(r'C:\Users\soug9\Desktop\Shcard Summer School\data\online+customer+store.txt',"rb") as fp :
        ocs = pickle.load(fp) 
        
with open(r'C:\Users\soug9\Desktop\Shcard Summer School\data\transaction+customer+store.txt',"rb") as fp :
        tcs = pickle.load(fp) 

ocs['online'] = [1]*len(ocs)
tcs['online'] = [0]*len(tcs)

ocs_tcs = pd.concat([ocs, tcs])

ocs_tcs_online = ocs_tcs[ocs_tcs['CLNN'].isin(total)]
ocs_online = ocs_tcs_online[ocs_tcs_online['online'] == 1]
tcs_online = ocs_tcs_online[ocs_tcs_online['online'] == 0]

ocs_tcs_online['UPJONG_GB_1'].value_counts()



















