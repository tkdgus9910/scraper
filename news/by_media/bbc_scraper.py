# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 16:09:35 2021

@author: tmlab
"""

import pandas as pd
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By

URL = 'https://www.bbc.co.uk/search?q=metaverse'

driver = webdriver.Chrome(executable_path='D:/OneDrive - 아주대학교/유틸리티/driver/chromedriver_94')
driver.get(url=URL)


#%%
result_df = pd.DataFrame()
page = 1

while True :
    
    sleep(2)
    
    for i in range(1,11) :
        
        i = str(i)
        path = '//*[@id="main-content"]/div[1]/div[3]/div/div/ul/li['+i +']/div/div/div[1]/div[1]/a'
        element = driver.find_element(By.XPATH, path)
        title = element.text
        url = element.get_attribute('href')
        
        path = '//*[@id="main-content"]/div[1]/div[3]/div/div/ul/li['+i +']/div/div/div[1]/div[2]/div/dl/div[1]'
        element = driver.find_element(By.XPATH, path)
        date = element.text
        result_df = result_df.append({'title' : title,
                                      'date' :date,
                                      'url' : url}, ignore_index=1)
    

    if page == 1 : path = '//*[@id="main-content"]/div[1]/div[4]/div/div/nav/div/div/div[4]/div/a/div'
    else : path = '//*[@id="main-content"]/div[1]/div[4]/div/div/nav/div/div/div[4]/div/a/div'
    
    print(page)
    
    button = driver.find_element(By.XPATH, path)
    button.click()
    
    page +=1
    
    #%%
    
    directory = "D:/github/media-scraper/output/"
    result_df.to_csv(directory + 'bbc_metaverse.csv', index = 0)