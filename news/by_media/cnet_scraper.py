# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 12:27:41 2021

@author: tmlab
"""

import pandas as pd
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By

q = 'apple ipad'
q = 'samsung galaxy tab'
URL = 'https://www.cnet.com/search/?query='+ q

driver = webdriver.Chrome(executable_path= 'D:/github/media-scraper/driver/chromedriver.exe')
driver.get(url=URL)

#%% get url
result_df = pd.DataFrame()
page = 1

while True :
    sleep(2)
    
    for i in range(1,11) :
        
        i = str(i)
        path = "//*[starts-with(@id, 'uid-')]/section["+i+"]/div/a"
        element = driver.find_element(By.XPATH, path)
        title = element.text
        url = element.get_attribute('href')
        
        try : 
            path = "//*[starts-with(@id, 'uid-')]/section["+i+"]/div/p[2]/span[2]"
            element = driver.find_element(By.XPATH, path)
            date = element.text
            
        except : date = ''
        result_df = result_df.append({'title' : title,
                                      'date' :date,
                                      'url' : url}, ignore_index=1)
    

    if page == 1 : path = '//*[@id="searchResultsdiv"]/div[3]/div[2]/a'
    else : path = '//*[@id="searchResultsdiv"]/div[3]/div[2]/a[2]'
    
    print(page)
    
    button = driver.find_element(By.XPATH, path)
    button.click()
    
    page +=1

#%%

directory = "D:/github/media-scraper/output/"
result_df.to_csv(directory + 'cnet_'+q+'.csv', index = 0)
