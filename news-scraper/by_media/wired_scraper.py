# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 12:27:41 2021

@author: tmlab
"""

import pandas as pd
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By

URL = 'https://www.wired.com/search/?q=metaverse&page=1&sort=score'

driver = webdriver.Chrome(executable_path='D:/OneDrive - 아주대학교/유틸리티/driver/chromedriver_94')
driver.get(url=URL)

#%%test

path = '//*[@id="app-root"]/div/div[4]/div/div[1]/div[2]/nav/ul/li/a/i'
button = driver.find_element(By.XPATH, path)
button.click()

#%%

# //*[@id="app-root"]/div/div[4]/div/div[1]/div[2]/div/ul/li[1]/div/a/h2
# //*[@id="app-root"]/div/div[4]/div/div[1]/div[2]/div/ul/li[2]/div/a/h2

result_df = pd.DataFrame()
page = 1

while True :
    
    for i in range(1,11) :
        
        i = str(i)
        path = '//*[@id="app-root"]/div/div[4]/div/div[1]/div[2]/div/ul/li['+i+']/div/a'
        element = driver.find_element(By.XPATH, path)
        url = element.get_attribute('href')
        text = element.text
        title = text.split("/n")[0]
        
        
        path = '//*[@id="app-root"]/div/div[4]/div/div[1]/div[2]/div/ul/li['+i+']/div/div/time'
        element = driver.find_element(By.XPATH, path)
        date = element.text
        
        result_df = result_df.append({'title' : title,
                                      'date' :date,
                                      'url' : url}, ignore_index=1)
    
    print(page)
    
    page +=1
    
    url ='https://www.wired.com/search/?q=metaverse&page='+str(page)+'&sort=score'
    driver.get(url=url)
    
    sleep(10)
    
    # //*[@id="app-root"]/div/div[4]/div/div[1]/div[2]/nav/ul/span[2]/li/a
#%%

result_df['title'] = [i.splitlines()[0] for i in result_df['title']]
    
directory = "D:/github/media-scraper/output/"
result_df.to_csv(directory + 'wired_metaverse.csv', index = 0)
