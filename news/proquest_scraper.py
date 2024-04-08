
from selenium import webdriver # selenium의 webdriver를 사용하기 위한 import
from selenium.webdriver.common.keys import Keys # selenium으로 키를 조작하기 위한 import

# 페이지 로딩을 기다리는데에 사용할 time 모듈 import
import time
import pandas as pd

from selenium.webdriver.common.by import By

directory = 'D:/data/BRM/proquest/'

file_name = 'samsung_magazine.csv'
data = pd.read_csv(directory+ file_name)


# 전처리 
data = data.loc[data['Language'] == 'ENG', : ].reset_index(drop = 1)
data['PubYear'] = data['PubDate'].apply(lambda x : int(x.split('-')[0]))
from collections import Counter 

c = Counter(data['PubYear'])

temp = pd.DataFrame(c.items()).sort_values(by = 0)


#%% 테스트 코드
# 크롬드라이버 실행
driver = webdriver.Chrome() 

#크롬 드라이버에 url 주소 넣고 실행
url = data['DocumentUrl'][1]
driver.get(url)

# 페이지가 완전히 로딩되도록 3초동안 기다림
time.sleep(3)

# 검색어 창을 찾아 search 변수에 저장 (xpath 이용방식)
item = driver.find_elements(By.XPATH, '//*[@id="fullTextZone"]/text')

for comment in item:
    print(comment.text)


    
#%% 데이터 수집

import numpy as np

data['Contents'] = [[] for _ in range(len(data))]

driver = webdriver.Chrome() 

for idx, url in enumerate(data['DocumentUrl']) : 
    
    if data['Contents'][idx] == [] :
        
        driver.get(url)
    
        # 페이지가 완전히 로딩되도록 5초동안 기다림
        time.sleep(5)
        
        # 검색어 창을 찾아 search 변수에 저장 (xpath 이용방식)
        item = driver.find_elements(By.XPATH, '//*[@id="fullTextZone"]/text')
        
        result = []
    
        for comment in item:
            result.append(comment.text)
            
        print(idx)
        
        if len(result) == 0 :
            driver = webdriver.Chrome() 
            
        else :     
            data['Contents'][idx] = result
            # 페이지가 완전히 로딩되도록 5초동안 기다림
            time.sleep(10)
    
    else : print(str(idx) +' pass')
    
#%%

temp = data['Contents']
temp = temp.apply(lambda x : x[0] if x != [] else np.nan)

from copy import copy

data_ = copy(data)
data_['Contents'] = data_['Contents'].apply(lambda x : x[0] if x != [] else np.nan)
data_.to_csv(directory + file_name + '_완료.csv')