# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 20:28:43 2020

@author: tmlab
"""

from GoogleNews import GoogleNews
from newspaper import Article
from datetime import datetime
from datetime import timedelta
from dateutil import relativedelta
import re
import pandas as pd
import os
import time

# resp = requests.get('http://example.com', proxies=proxies )


class Object : 
        
    def __init__(self, searchQuery_, directory):
        self.result = pd.DataFrame()
        self.searchQuery_ = searchQuery_
        self.directory = directory
    
    def scrape(self) :
        pass
    
    def chdir(self, directory):
        self.directory = directory
    
    def save(self , directory) :        
        self.result.to_csv(self.directory + self.searchQuery_[0] + ".csv", index = False)
    
class googleArticle(Object) :
    
    # def __init__(self, searchQuery_, st_year, ed_year):
    #     Object.__init__(self, searchQuery_, st_year, ed_year)
        
    def metaScrape(self) : 
        
        for i in range(len(self.searchQuery_)) : 
    
            Q = self.searchQuery_[i]
            
            googlenews = GoogleNews(lang='en', region='US')
            googlenews.set_period('7d')
            googlenews.set_encode('utf-8')
            
            for month in list(range(0,6)) : 
                st_month = str(month*2 +1)
                end_month = str(month*2 +2)
                
                googlenews.set_time_range(start = st_month + '/01/2020', end =  end_month + '/31/2020')
                
                
                j = 0 # j 초기화
                    
                while True :
                    
                    print("{}번째 쿼리 중 {}페이지 수집중".format(i+1,j))
                    
                    googlenews.search(Q)
                    
                    googlenews.getpage(j)
                    
                    temp = googlenews.result()
                    temp = pd.DataFrame(temp)
                    googlenews.clear()
                    
                    temp['query'] = Q
                    self.result = pd.concat([self.result, temp])
                    self.result = self.result.drop_duplicates("title")
                    self.result = self.result.reset_index(drop = True)
                    
                    if temp.shape[1] <= 1 :
                        break
                    else :
                        j += 1
                                    
                time.sleep(2)
                
    def contentScrape(self) :
            
        self.result['content'] = ""
        
        i = 0
        
        for url in self.result['link'] :
            
            article = Article(url)
            article.download()
            try : article.parse()
            except : continue
            self.result['content'][i] = article.text
            i += 1
            print("전체 데이터 {}개의 데이터 중 {}번째 수집중".format(len(self.result),i))
        
        for i in range(len(self.result)) :
            
            url = self.result['link'][i]
            content = self.result['content'][i]
            
            if len(content) > 1 : continue
        
            else : 
            
                article = Article(url)
                article.download()
                try : article.parse()
                except : continue
                self.result['content'][i] = article.text
                
                print("전체 데이터 {}개의 데이터 중 {}번째 기사 재수집중".format(len(self.result),i))
            
#%% 1-A. 제품기사 수집기

# 경로 초기화 
os.chdir(os.path.dirname(os.path.abspath(__file__)))

directory = "D:/github/media-scraper/output/"

# search_query = ['"Metaverse" site:www.nytimes.com']
# search_query = ['samsung galaxy tab', 'apple ipad']
search_query = ['apple ipad']

article = googleArticle(search_query, directory)

article.metaScrape()

#%% 추가 수집

i = 0
Q = search_query[i]
j = 29 # j 초기화

while True :
    
    print("{}번째 쿼리 중 {}페이지 수집중".format(i+1,j))
    
    googlenews = GoogleNews()
    
    googlenews.search(Q)
    
    googlenews.getpage(j)
    
    temp = googlenews.result()
    temp = pd.DataFrame(temp)
    googlenews.clear()
    
    temp['query'] = Q
    article.result = pd.concat([article.result, temp])
    article.result = article.result.drop_duplicates("title")
    article.result = article.result.reset_index(drop = True)
    
    if temp.shape[1] <= 1 :
        break
    else :
        j += 1
        
    time.sleep(3)
            
article.contentScrape()

#%% 2. 저장
# article.result.to_csv(directory + "3d print_article.csv", index = False)
article.result.to_csv(directory + "NYT_metaverse.csv", index = False)

#%% 3. load

directory = "D:/github/media-scraper/output/"

import pandas as pd
article = pd.read_csv(directory + "cnet_article.csv")



#%%

yyyymmdd = datetime(2019, 1, 1, 0, 0, 0)
print(yyyymmdd)
for k in range(1,13) :
    
    yyyymmdd = yyyymmdd + relativedelta.relativedelta(months=1)
    thismonth_lastday = yyyymmdd - timedelta(seconds=1)
    
    startday_thismonth = thismonth_lastday.strftime('%Y%m') + "01"
    lastday_thismonth = thismonth_lastday.strftime('%Y%m%d')
    print(startday_thismonth)
    
    