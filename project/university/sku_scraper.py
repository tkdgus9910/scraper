# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 12:27:41 2021

@author: tmlab
"""

import pandas as pd
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
import numpy as np


# 1. url 연결

URL = 'https://professor.skku.edu/researcher/professorList.do?mode=list&jojikCode1=3163&categoryId=G&srProfessorType='


driver = webdriver.Chrome(executable_path= 'D:/github/chromedriver.exe')
driver.get(url=URL)

result_df = pd.DataFrame()

#%% 2. 수집

i = 1

while True :
    
    sleep(3)
    
    path = '//*[@id="jwxe_main_content"]/div/div/div/div[3]/div/div['+str(i)+']'
    element = driver.find_element(By.XPATH, path)
    
    #직위
    try : spot = element.find_element(By.CLASS_NAME, 'jg').text
    except : spot = np.nan
    #학과
    try : department = element.find_element(By.CLASS_NAME, 'dtj').text
    except : department = np.nan
    
    #이름
    path_ = path + '/dl/dd[1]/ul/li[2]/span'
    element = driver.find_element(By.XPATH, path_)
    name = element.text
    
    #이동
    path_ = path + '/dl/dt/a[1]'
    element = driver.find_element(By.XPATH, path_)
    element.click()
    sleep(2)
    #추가수집-학력/경력
    elements = driver.find_elements(By.CLASS_NAME, 'education_view_box')
    if type(elements) != list : 
        elements = [elements]
    
    education = np.nan
    career = np.nan
    
    for element in elements :
        
        key = element.find_element(By.CLASS_NAME , 'h4-tit01').text
        
        if key == '학력' :
            education = element.find_element(By.CLASS_NAME , 'ul-type01').text
            
        elif key == '약력/경력' : 
            career = element.find_element(By.CLASS_NAME , 'ul-type01').text
    
    #추가수집-경력
    result_df = result_df.append({'이름' : name,
                                  '학과' : department,
                                  '직위' : spot,
                                  '학력' : education,
                                  '경력' : career, 
                                  '현 재직기관' : '소프트웨어융합대학'}, ignore_index=1)
    
    driver.back()
    i += 1
    
#%% 3. 데이터 변환

import re 
import numpy as np 

result_df['대학명'] = '성균관대학교'

result_df['박사_학위수여대학'] = np.nan
result_df['박사_전공'] = np.nan
result_df['박사_학위수여년도'] = np.nan

result_df['석사_학위수여대학'] = np.nan
result_df['석사_전공'] = np.nan
result_df['석사_학위수여년도'] = np.nan

result_df['학사_학위수여대학'] = np.nan
result_df['학사_전공'] = np.nan
result_df['학사_학위수여년도'] = np.nan


#1. 학력 분류

for idx, row in result_df.iterrows() : 
    
    education = row['학력']
    if type(education) == float : continue
    education = education.split('\n')
    education_dict = {}
    
    # for edu in education :
        
    #     bachelor = ['B.S.', '학사', 'B. S.', 'BS', 'B.S', 'Bachelor', 'B.E.']
    #     master = ['M.S.', '석사' , 'MBA', 'MS', 'M.A.', 'Master', 'M.Arch.', 'M.S', 'M. S.']
    #     doctor = ['Ph.D', '박사', 'Ph. D.', 'Dr.', 'PhD']
        
    #     if any(i in edu for i in bachelor) : 
    #         education_dict['학사'] = edu
    #         result_df['학사_정보'][idx] = edu
    #     elif any(i in edu for i in master) : 
    #         education_dict['석사'] = edu
    #         result_df['석사_정보'][idx] = edu
    #     elif any(i in edu for i in doctor) : 
    #         education_dict['박사'] = edu
    #         result_df['박사_정보'][idx] = edu
    #     else : 
    #         education_dict['기타'] = edu
            

    # for k,v in education_dict.items() :
        
    #     if k == '기타' : continue
        
    #     col = k+'_'+'학위수여대학'
    #     pat = r'[\w]+학교'
    #     try : 
    #         match = re.findall(pat, edu)[0]
    #         result_df[col][idx] = match
    #     except : pass
    
    #     col = k+'_'+'학위수여년도'
    #     pat = r'\d+'
    #     try : 
    #         match = re.findall(pat, edu)
    #         match = "_".join(match)
    #         result_df[col][idx] = match
    #     except : pass
        
#%%

result_df = result_df[['대학명','이름','현 재직기관', '학과', '직위', 
                       '학력', '박사_학위수여대학', '박사_전공', '박사_학위수여년도', '석사_학위수여대학', '석사_전공', '석사_학위수여년도', 
                       '학사_학위수여대학', '학사_전공', '학사_학위수여년도','경력']]


result_df['경력_재직기관'] = np.nan
result_df['경력_직위'] = np.nan
result_df['경력_재직기간(시작, 끝)'] = np.nan

#%%

# result_df['경력_정보'] = result_df['경력'].apply(lambda x : x.split('\n') if type(x) != float  else x)
#%%
directory = 'D:/OneDrive - SNU'
result_df.to_excel(directory + '/skku_result.xlsx')
#%%
try : result_df['학사'][idx] = education_dict['학사']
except : pass

try : result_df['석사'][idx] = education_dict['석사']
except : pass

try : result_df['박사'][idx] = education_dict['박사']
except : pass

try : result_df['학력_기타'][idx] = education_dict['기타']
except : pass




#%%
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
