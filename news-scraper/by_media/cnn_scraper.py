# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 16:52:16 2021

@author: tmlab
"""


import pandas as pd
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By

URL = 'https://edition.cnn.com/search?q=metaverse'

driver = webdriver.Chrome(executable_path='D:/OneDrive - 아주대학교/유틸리티/driver/chromedriver_94')
driver.get(url=URL)

#%% page based

result_df = pd.DataFrame()
page = 1

while True :
    
    sleep(2)
    
    for i in range(1,11) :
        
        i = str(i)
        path = '/html/body/div[5]/div[2]/div/div[2]/div[2]/div/div[3]/div['+i +']/div[2]/h3/a'
        element = driver.find_element(By.XPATH, path)
        title = element.text
        url = element.get_attribute('href')
        
        path = '/html/body/div[5]/div[2]/div/div[2]/div[2]/div/div[3]/div['+i +']/div[2]/div[1]/span[2]'
        element = driver.find_element(By.XPATH, path)
        date = element.text
        result_df = result_df.append({'title' : title,
                                      'date' :date,
                                      'url' : url}, ignore_index=1)
    

    if page == 1 : path = '/html/body/div[5]/div[2]/div/div[2]/div[2]/div/div[5]/div/div[3]'
    else : path = '/html/body/div[5]/div[2]/div/div[2]/div[2]/div/div[5]/div/div[3]'
    
    print(page)
    
    button = driver.find_element(By.XPATH, path)
    button.click()
    
    page +=1
    
    #%%
        
    directory = "D:/github/media-scraper/output/"
    result_df.to_csv(directory + 'cnn_metaverse.csv', index = 0)