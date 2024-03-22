# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 16:19:40 2021

@author: tmlab
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 16:09:35 2021

@author: tmlab
"""


import pandas as pd
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By

URL = 'https://www.nytimes.com/search?query=metaverse'

driver = webdriver.Chrome(executable_path='D:/OneDrive - 아주대학교/유틸리티/driver/chromedriver_94')
driver.get(url=URL)

#%% 아래로 이동
from selenium.webdriver.common.keys import Keys

while (1) :
    
    driver.find_element_by_xpath('//body').send_keys(Keys.CONTROL+Keys.END)

    sleep(1)
    path = '//*[@id="site-content"]/div/div[2]/div[2]/div/button'
    button = driver.find_element(By.XPATH, path)
    button.click()

#%% 저장
    
result_df = pd.DataFrame()
i = 1
while True :
    # sleep(2)
    print(i)       
    #url
    i_ = str(i)
    try : 
        path = '//*[@id="site-content"]/div/div[2]/div/ol/li['+i_+']/div/div/div/a/h4'
        element = driver.find_element(By.XPATH, path)
        title = element.text
    
        path = '//*[@id="site-content"]/div/div[2]/div/ol/li['+i_+']/div/div/div/a'
        element = driver.find_element(By.XPATH, path)
        url = element.get_attribute('href')
        
        path= '//*[@id="site-content"]/div/div[2]/div/ol/li['+i_+']/div/span'
        element = driver.find_element(By.XPATH, path)
        date = element.text
        
        result_df = result_df.append({'title' : title,
                                      'date' :date,
                                      'url' : url}, ignore_index=1)
    except : pass

    i+=1
    if i > 300 : break

#%% save

directory = "D:/github/media-scraper/output/"
result_df.to_csv(directory + 'nyt_metaverse.csv', index = 0)