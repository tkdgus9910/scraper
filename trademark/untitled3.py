# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 17:51:00 2023

@author: tmlab
"""

import pandas as pd

directory = 'D:/OneDrive - SNU/db/patent/태은/'

data = pd.read_excel(directory + 'C26129기업특허.xls')
data['CPC분류_prep'] = data['CPC분류'].apply(lambda x : x.split('|'))
data['CPC분류_prep'] = data['CPC분류_prep'].apply(lambda x : [i.split(' ')[0] for i in x])
 
data_applicant = data.groupby(['출원인'])[['CPC분류_prep']].agg(lambda x : sum(x, []))

#%%
from collections import Counter

#기업별 cpc분포
data_applicant['CPC분류_counter'] = data_applicant['CPC분류_prep'].apply(lambda x : Counter(x))

#전체 cpc 분포를 보고싶을 때
c = Counter([x for xs in data_applicant['CPC분류_counter'] for x in set(xs)])