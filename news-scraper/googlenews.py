# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 15:14:27 2022

@author: tmlab
"""

# googlenews.set_period('7d')

#%% 개별 수집

from GoogleNews import GoogleNews

googlenews = GoogleNews(lang='en', region='US')
googlenews.set_encode('utf-8')

googlenews.set_time_range(start = '01/01/2022', end = '12/31/2022')
q = 'electric vehicle battery'
# q = '6G communication scenario'
# q = '6G communication use-case'

googlenews.search(q)
# googlenews.get_news(q)


#%% 연별 수집
from GoogleNews import GoogleNews
import time
import pandas as pd

googlenews = GoogleNews(lang='en', region='US')
googlenews.set_encode('utf-8')

q_list = ['6G technology', 
          '6G communication scenario', 
          '6G communication use-case']

googlenews.set_time_range(start = '01/01/2019', end = '12/31/2019')

result_df = pd.DataFrame()

for q in q_list :
    googlenews.search(q)
    
    for page in range(1, 11) :
        result = googlenews.page_at(page)
        for res in result:
            # res['month'] = month
            result_df = result_df.append(res, ignore_index = 1)

result_df = result_df.drop_duplicates(['desc']).reset_index(drop = 1)

directory = 'G:/공유 드라이브/TILAB/프로젝트/2022/ETRI/2차보고서[20220629]/기사 데이터/'
result_df.to_csv(directory + '6G_scenario_2019.csv')

#%% 월별 수집
import time
import pandas as pd
# print(googlenews.total_count())
# googlenews.results(sort=True)
googlenews.set_encode('utf-8')
# q = 'apple ipad'
q = 'samsung galaxy tab'
result_df = pd.DataFrame()


for month in range(7, 13) : 
    
    month = str(month)
    print('the month is ', month)
    googlenews.set_time_range(start = month + '/01/2020', end = month + '/31/2020')
    googlenews.search(q)
    time.sleep(5)
    
    for page in range(1, 11) :
        result = googlenews.page_at(page)
        for res in result:
            res['month'] = month
            result_df = result_df.append(res, ignore_index = 1)
        

result_df = result_df.drop_duplicates('title').reset_index(drop = 1)
directory = 'D:/github/media-scraper/output/'
result_df.to_csv(directory + 'news_'+ q+'.csv', index = 0)


#%%
directory = 'D:/github/media-scraper/output/' 
result_df = pd.read_csv(directory + 'news_apple_ipad.csv')
#%% # 텍스트 다운
# result_df_ = result_df.loc[(result_df['title'].str.contains('Tab'))|
#                             (result_df['title'].str.contains('tablet')), :].reset_index(drop = 1)

result_df_ = result_df.loc[(result_df['title'].str.contains('iPad')), :].reset_index(drop = 1)

result_df_['text'] = ''

#%% 컨텐츠 다운로드 1. 데이터 로드 및 필터
import os
directory = 'G:/공유 드라이브/TILAB/프로젝트/2022/ETRI/2차보고서[20220629]/기사 데이터/'

file_list = os.listdir(directory)
file_list = [i for i in file_list if '.csv' in i]

data = pd.DataFrame()

for f in file_list :
    
    temp_data = pd.read_csv(directory + f)
    data = pd.concat([data, temp_data], axis = 0)

data = data.iloc[:,1:].reset_index(drop = 1)
data = data.drop_duplicates(['desc']).reset_index(drop = 1)
data_ = pd.DataFrame()

for idx, row in data.iterrows() :
    
    if '6G' in row['title'] :
        data_ = data_.append(row)

data_['year'] = data_['date'].apply(lambda x : x.split(", ")[1] if ', ' in x else '2022')

#%% 컨텐츠 다운로드 시작 

from newspaper import Config
from newspaper import Article

data_['text']= ''

for idx,row in data_.iterrows()     :
    
    url = row['link']
    
    try:
        article = Article(url)
        article.download()
        article.parse()
        data_['text'][idx] = article.text
        
    except : print(idx)
    

#%%
        
# data_ = data_.loc[data_['text'] != '',:]

data_.to_csv(directory + '6G_article_.csv', index = 0)