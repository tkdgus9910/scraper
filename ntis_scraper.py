# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 12:27:41 2021

@author: tmlab
"""

import pandas as pd
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By

#%% 1. url 연결

URL = 'https://eng.snu.ac.kr/professor?&title='


driver = webdriver.Chrome(executable_path= 'D:/github/chromedriver.exe')
driver.get(url=URL)


#%% 2. 수집

result_df = pd.DataFrame()


while True :
    
    sleep(3)
    
    for i in range(1,6) :
        
        sleep(2)
        
        i = str(i)
        path = '//*[@id="block-system-main"]/div/div/div[2]/ul/li['+i+']/dl/dt/a'
        element = driver.find_element(By.XPATH, path)
        name = element.text
        element.click()
        
        #수집
        path = '//*[@id="block-system-main"]/div'
        element = driver.find_element(By.XPATH, path)
        contents = element.text
        
        
        result_df = result_df.append({'이름' : name,
                                              'contents' :contents}, ignore_index=1)
        
        driver.back()
    
    # next page
    element = driver.find_element_by_class_name('pager-next')
    element.click()
    
#%% 3. 데이터 변환

import re 
import numpy as np 

result_df['대학명'] = '서울대학교'
result_df['학과'] = np.nan
result_df['직위'] = np.nan
result_df['박사'] = np.nan
result_df['석사'] = np.nan
result_df['학사'] = np.nan
result_df['학력_기타'] = np.nan
result_df['경력'] = np.nan
result_df['주전공'] = np.nan
result_df['부전공'] = np.nan
result_df['주요연구분야'] = np.nan


# 주요 연구분야

def findall_nan(pat, paragraph) :
    pat = pat
    match = re.findall(pat, p1)
    
    if len(match) >= 1:
        match = re.findall(pat, p1)[0]
        match = match.split(' ')[1:]
        match = ' '.join(match)
    
    else : match = np.nan
    
    return match

for idx, row in result_df.iterrows() :
    
    text = row['contents']
    
    paragraph = text.split('\n\n')
    para_dict = {}
    
    for p in paragraph :
        key = p.split('\n')[0]
        if '세부정보' in key : 
            key = '세부정보'
        value = "\n".join(p.split('\n')[1:])
        para_dict[key] = value 
    
    p1 = para_dict['세부정보']
    
    # 세부정보
    pat = r'소속\s[가-힣]+'
    match = findall_nan(pat, p1)
    result_df['학과'][idx] = match
    
    pat = r'직위\s[가-힣]+'
    match = findall_nan(pat, p1)
    result_df['직위'][idx] = match
    
    pat = r'주전공\s[가-힣]+'
    match = findall_nan(pat, p1)
    result_df['주전공'][idx] = match
    
    pat = r'부전공\s[가-힣]+'
    match = findall_nan(pat, p1)
    result_df['부전공'][idx] = match
    
    # 학력
    if len(p1.split('학력\n')) >= 2 : 
        education = p1.split('학력\n')[1]
        education = education.split('\n')
        education_dict = {}
        
        for edu in education :
            
            bachelor = ['B.S.', '학사', 'B. S.', 'BS', 'B.S', 'Bachelor', 'B.E.']
            master = ['M.S.', '석사' , 'MBA', 'MS', 'M.A.', 'Master', 'M.Arch.', 'M.S', 'M. S.']
            doctor = ['Ph.D', '박사', 'Ph. D.', 'Dr.', 'PhD']
            
            if any(i in edu for i in bachelor) : 
                education_dict['학사'] = edu
            elif any(i in edu for i in master) : 
                education_dict['석사'] = edu
            elif any(i in edu for i in doctor) : 
                education_dict['박사'] = edu
            else : 
                education_dict['기타'] = edu
        
        try : result_df['학사'][idx] = education_dict['학사']
        except : pass
    
        try : result_df['석사'][idx] = education_dict['석사']
        except : pass
    
        try : result_df['박사'][idx] = education_dict['박사']
        except : pass
    
        try : result_df['학력_기타'][idx] = education_dict['기타']
        except : pass
        
    # 경력
    
    try : result_df['경력'][idx] = para_dict['경력']
    except : pass
    
    try : result_df['주요연구분야'][idx] = para_dict['주요 연구분야']
    except : pass
    

#%%
# match = match.split(' ')[1]





#%%

directory = "D:/github/media-scraper/output/"
result_df.to_csv(directory + 'cnet_'+q+'.csv', index = 0)
