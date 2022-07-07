# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 13:06:39 2021

@author: tmlab
"""

if __name__ == '__main__':
    
    import pandas as pd
    from selenium import webdriver
    from time import sleep
    from selenium.webdriver.common.by import By

    import os
    
    directory = os.path.dirname(os.path.abspath(__file__))
    directory = directory.replace("\\", "/") # window
    os.chdir(directory)    
    
#%%

    URL = 'https://www.cnbc.com/search/?query=metaverse&qsearchterm=metaverse'
    
    driver = webdriver.Chrome(executable_path='./driver/chromedriver')
    driver.get(url=URL)

#%%
    from selenium.webdriver.common.keys import Keys
    
    driver.find_element_by_xpath('//body').send_keys(Keys.CONTROL+Keys.END)
    #%%
    
    result_df = pd.DataFrame()
    i = 1
    
    while True :
        # sleep(2)
        print(i)       
        #url
        i_ = str(i)
        path = '//*[@id="searchcontainer"]/div['+i_+']/div/div[2]/div[2]/a/span'
        element = driver.find_element(By.XPATH, path)
        title = element.text
        
        path = '//*[@id="searchcontainer"]/div['+i_+']/div/div[2]/div[2]/a'
        element = driver.find_element(By.XPATH, path)
        url = element.get_attribute('href')
        
        try :
            path= '//*[@id="searchcontainer"]/div['+i_+']/div/div[2]/span/span[2]'
            element = driver.find_element(By.XPATH, path)
            date = element.text
        except :
            path= '//*[@id="searchcontainer"]/div['+i_+']/div/div[2]/span/span'
            
            element = driver.find_element(By.XPATH, path)
            date = element.text
            
        result_df = result_df.append({'title' : title,
                                      'date' :date,
                                      'url' : url}, ignore_index=1)
        i+=1
        
#%% save

directory = "D:/github/media-scraper/output/"
result_df.to_csv(directory + 'cnbc_metaverse.csv', index = 0)

 