# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 16:09:35 2021

@author: tmlab
"""

if __name__ == '__main__':
    
    import pandas as pd
    from selenium import webdriver
    from time import sleep
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    import os
    import time

    
    directory = os.path.dirname(os.path.abspath(__file__))
    directory = directory.replace("\\", "/") # window
    os.chdir(directory)    
    
    driver = webdriver.Chrome(executable_path='./driver/chromedriver')

    q = 'samsung galaxy tab'

    URL = 'https://www.forbes.com/search/?q=' + q
    driver.get(url=URL)

    #%% 아래로 이동    
    while True :
     
        driver.find_element_by_xpath('//body').send_keys(Keys.CONTROL+Keys.END)
    # more article
        path = '/html/body/div[1]/main/div[1]/div[1]/div[5]'
        button = driver.find_element(By.XPATH, path)
        button.click()
        time.sleep(3)
        
    #%%
    
    result_df = pd.DataFrame()
    i = 1
    
    while True :
        # sleep(2)
        print(i)       
        #url
        i_ = str(i)
        path = '/html/body/div[1]/main/div[1]/div[1]/div[4]/div/article['+i_+']/div[1]/h3/a'
        element = driver.find_element(By.XPATH, path)
        title = element.text
        
        # path = '//*[@id="searchcontainer"]/div['+i_+']/div/div[2]/div[2]/a'
        # element = driver.find_element(By.XPATH, path)
        url = element.get_attribute('href')
        
        path= '/html/body/div[1]/main/div[1]/div[1]/div[4]/div/article['+i_+']/div[1]/div[1]'
        element = driver.find_element(By.XPATH, path)
        date = element.text
        
        result_df = result_df.append({'title' : title,
                                      'date' :date,
                                      'url' : url}, ignore_index=1)
        i+=1
    
     #%% save
    
    directory = "D:/github/media-scraper/output/"
    result_df.to_csv(directory + 'forbes_'+ q +'.csv', index = 0)