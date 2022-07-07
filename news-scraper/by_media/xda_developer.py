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
q = 'samsung+galaxy+tab'
URL = 'https://www.xda-developers.com/search/'+ q

driver = webdriver.Chrome(executable_path= 'D:/github/media-scraper/driver/chromedriver.exe')
driver.get(url=URL)

#%%

path = '//*[@class="next page-numbers"]'
button = driver.find_element(By.XPATH, path)
button.click()
#%%
# path = "//*[starts-with(@id, 'post-')]/div[2]/h4/a" # title
# elements = driver.find_elements(By.XPATH, path)
# title = elements[11].text

# path = "//*[starts-with(@id, 'post-')]/div[2]/div/span[2]" # date
# elements = driver.find_elements(By.XPATH, path)
# title = elements[11].text

path = "//*[starts-with(@id, 'post-')]/div[2]/h4/a" # date
elements = driver.find_elements(By.XPATH, path)
url = elements[11].get_attribute('href')


#%% get url

result_df = pd.DataFrame()
page = 1

while True :
    
    sleep(5)
    
    path = "//*[starts-with(@id, 'post-')]/div[2]/h4/a"
    elements = driver.find_elements(By.XPATH, path)
    
    path = "//*[starts-with(@id, 'post-')]/div[2]/div/span[2]" # date
    elements_ = driver.find_elements(By.XPATH, path)
    # title = elements[11].text
    
    for idx,item in enumerate(elements) : 
        element = item
        title = element.text
        url = element.get_attribute('href')
        date = elements_[idx].text
        
        result_df = result_df.append({'title' : title,
                              'date' :date,
                              'url' : url}, ignore_index=1)
    
    print(page)
    
    path = '//*[@class="next page-numbers"]'
    button = driver.find_element(By.XPATH, path)
    button.click()
    
    page +=1

#%%

result_df_ = result_df.loc[result_df['date'], :]
#%%

directory = "D:/github/media-scraper/output/"
result_df.to_csv(directory + 'cnet_'+q+'.csv', index = 0)
