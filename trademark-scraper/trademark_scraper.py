# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 22:46:58 2021

@author: tmlab
"""
import pandas as pd
import requests
from urllib.parse import urlencode, quote_plus
import xmltodict

key = 'PLkTuNb8ws1hTyHsOXZTrJX39gWk0wfexHpUyn5Q00E='

directory = 'D:/아주대학교/tmlab - 문서/프로젝트/2021/산업분석/가전/'

#%% 1. 사업자등록번호 -> 특허고객번호 추출 / API 월 1,000건
db_dict = pd.read_excel(directory + '가전 데이터_추합_삼엘제외(0917).xlsx', None);
db = db_dict['class']

db['특허고객번호'] = ''
db['법인번호'] = ''
# db['사업자등록번호'] = ''

for idx, row in db.iterrows() : 
    
    ID = row['사업자등록번호']
    ID = str(ID).split('.')[0] 
    if ID == 'nan' : continue
    ID = ID[0:3] + '-' + ID[3:5] + '-' + ID[5:]
    
    url_list = []
    url_list.append('http://plus.kipris.or.kr/openapi/rest/CorpBsApplicantService/') 
    url_list.append('corpBsApplicantInfoV3')
    url_list.append('?BusinessRegistrationNumber=')
    
    BusinessRegistrationNumber= ID
    url_list.append(BusinessRegistrationNumber)
    url_list.append('&accessKey=')
    url_list.append(key)
    
    url = ''
    for i in url_list : url += i
    response = requests.get(url)
    
    try : 
        data_dict = xmltodict.parse(response.content)
        applicantCode = data_dict['response']['body']['items']['corpBsApplicantInfo']['ApplicantNumber']
        corporationNumber = data_dict['response']['body']['items']['corpBsApplicantInfo']['CorporationNumber']
        
        db['사업자등록번호'][idx] = ID
        db['특허고객번호'][idx] = applicantCode
        db['법인번호'][idx] = corporationNumber
        
    except : 

        db['사업자등록번호'][idx] = ID
    
    print(idx, '완료')

db_dict['class'] = db
    
# 저장

writer = pd.ExcelWriter(directory + '가전 데이터_추합_삼엘제외(0917)_특허번호 추가.xlsx', 
                        engine='xlsxwriter')

for key in db_dict.keys() :
    temp = db_dict[key]
    temp.to_excel(writer , sheet_name = key, index = 0)


writer.save()
writer.close()

#%% 2. 사업자등록번호 -> 법인번호 추출 / scrape

from selenium import webdriver
from time import sleep

URL = 'https://bizno.net/'

driver = webdriver.Chrome(executable_path='D:/OneDrive - 아주대학교/driver/chromedriver_94')
driver.get(url=URL)

# 특허고객번호가 없는 기업 사업자등록번호 추출
BRN_list = []

for idx, row in db.iterrows() :
    if row['특허고객번호'] != '' : continue
    else: 
        if row['사업자등록번호'] != ' ' : BRN_list.append(row['사업자등록번호'])
       
#BRN to CN

BRN2CN_dict = {}

for BRN in BRN_list :
    
    # 검색어 입력
    path = '//*[@id="query"]'
    search_box = driver.find_element_by_xpath(path)
    query = BRN
    search_box.send_keys(query)
    
    # 클릭
    path = '//*[@id="home"]/div[2]/div/div/form/div/div[2]/button'
    button = driver.find_element_by_xpath(path)
    button.click()
    
    # 이동
    path = '/html/body/section[2]/div/div/div[1]/div[1]/div/div/div/a/h4'
    try : 
        button = driver.find_element_by_xpath(path)
        button.click()
    except : continue

    # 광고
    main = driver.window_handles 
    for handle in main: 
        if handle != main[0]: 
            driver.switch_to_window(handle) 
            driver.close()

    # 법인번호
    path = '/html/body/section[2]/div/div/div[1]/div[1]/div/table/tbody/tr[8]/td'
    try : 
        posting = driver.find_element_by_xpath(path)        
        CN = posting.text
    except : continue

    BRN2CN_dict[BRN] = CN

    # 뒤로가기
    driver.back()
    
    sleep(2)

# 저장

for k,v in BRN2CN_dict.items() :
    
    idx = db.loc[db['사업자등록번호'] == k,:].index[0]
    db['법인번호'][idx] = v


db_dict['class'] = db

writer = pd.ExcelWriter(directory + '가전 데이터_추합_삼엘제외(0923)_특허번호 추가.xlsx', 
                        engine='xlsxwriter')

for key in db_dict.keys() :
    temp = db_dict[key]
    temp.to_excel(writer , sheet_name = key, index = 0)


writer.save()
writer.close()
#%% 3. 법인번호 -> 특허고객번호 추출 / API
import numpy as np

db_dict = pd.read_excel(directory + '가전 데이터_추합_삼엘제외(0923)_특허번호 추가.xlsx', None);
db = db_dict['class']

for idx, row in db.iterrows() : 
    
    if str(row['특허고객번호']) != 'nan' : continue
    
    else : 
        ID = row['사업자등록번호']
        
        if ID == ' ' : continue
    
        url_list = []
        url_list.append('http://plus.kipris.or.kr/openapi/rest/CorpBsApplicantService/') 
        
        # url_list.append('corpBsApplicantInfoV3')
        # url_list.append('?BusinessRegistrationNumber=')
        # BusinessRegistrationNumber= ID
        # url_list.append(BusinessRegistrationNumber)
        
        url_list.append('corpBsApplicantInfoV2')
        url_list.append('?CorporationNumber=')
        CorporationNumber = row['법인번호']
        url_list.append(CorporationNumber)
        
        url_list.append('&accessKey=')
        url_list.append(key)
        
        url = ''
        for i in url_list : url += i
        response = requests.get(url)
        
        try : 
            data_dict = xmltodict.parse(response.content)
            applicantCode = data_dict['response']['body']['items']['corpBsApplicantInfo']['ApplicantNumber']
            
            db['특허고객번호'][idx] = applicantCode
            
            print(idx, '완료')
            
        except : print(idx, '실패')
        db['사업자등록번호'][idx] = ID
    

db_dict['class'] = db
    
# 저장

writer = pd.ExcelWriter(directory + '가전 데이터_추합_삼엘제외(0923)_특허번호 추가.xlsx', 
                        engine='xlsxwriter')

for key in db_dict.keys() :
    temp = db_dict[key]
    temp.to_excel(writer , sheet_name = key, index = 0)


writer.save()
writer.close()



#%% 4. 상표권 추출 / API

import pandas as pd
import requests
import xmltodict

def make_query(ApplicantNumber, pageNo = 1) :
    
    url_list = []
    url_list.append('http://plus.kipris.or.kr/kipo-api/kipi/trademarkInfoSearchService/') 
    url_list.append('getAdvancedSearch')
    
    url_list.append('?applicantName=')
    url_list.append(ApplicantNumber)
    
    url_list.append('&application=true') # 출원
    url_list.append('&registration=true') # 등록
    url_list.append('&refused=true') # 거절
    url_list.append('&expiration=true') # 소멸
    url_list.append('&withdrawal=true') # 취하
    url_list.append('&publication=true') # 공고
    url_list.append('&cancel=true') # 무효
    url_list.append('&abandonment=true') #포기
    url_list.append('&trademark=true')
    url_list.append('&serviceMark=true')
    url_list.append('&businessEmblem=true')
    url_list.append('&collectiveMark=true')
    url_list.append('&geoOrgMark=true')
    url_list.append('&trademarkServiceMark=true')
    url_list.append('&certMark=true')
    url_list.append('&geoCertMark=true')
    url_list.append('&internationalMark=true')
    url_list.append('&character=true')
    url_list.append('&figure=true')
    url_list.append('&compositionCharacter=true')
    url_list.append('&figureComposition=true')
    url_list.append('&fragrance=true')
    url_list.append('&sound=true')
    url_list.append('&color=true')
    url_list.append('&colorMixed=true')
    url_list.append('&dimension=true')
    url_list.append('&hologram=true')
    url_list.append('&invisible=true')
    url_list.append('&motion=true')
    url_list.append('&visual=true')
    url_list.append('&applicationDate=20100101~20201231')
    url_list.append('&pageNo=')
    url_list.append(str(pageNo))
    
    key = 'PLkTuNb8ws1hTyHsOXZTrJX39gWk0wfexHpUyn5Q00E='
    url_list.append('&ServiceKey=')
    url_list.append(key)
    
    url = ''
    for i in url_list : url += i
    
    return(url)

db_dict = pd.read_excel(directory + '가전 데이터_추합_삼엘제외(0923)_특허번호 추가.xlsx', None);
db = db_dict['class']
db_trademark = pd.DataFrame()


for idx, row in db.iterrows() : 
    
    if str(row['특허고객번호']) == 'nan' : 
        print(idx, '실패(특허고객번호 X)')
        continue
    
    ApplicantNumber = str(int(row['특허고객번호'])) 
    
    url = make_query(ApplicantNumber)
    response = requests.get(url)
    data_dict = xmltodict.parse(response.content)
    
    try : 
        dict_list = data_dict['response']['body']['items']['item'] # 상표권 Dict list
    except : 
        print(idx, '실패(상표권 X)')
        continue
    
    if type(dict_list) == list :
        for DICT in dict_list : 
            DICT['ID'] = ApplicantNumber 
            db_trademark = db_trademark.append(DICT, ignore_index=1).reset_index(drop = 1)
    else : 
        dict_list['ID'] = ApplicantNumber 
        db_trademark = db_trademark.append(dict_list, ignore_index=1).reset_index(drop = 1)
        
    
    temp = data_dict['response']['count']['totalCount']
    page_max = int(int(temp)/20)+1 # 페이지 숫자
    
    if page_max > 1 : # 20개 이상일 때
        for i in range(2, page_max+1) :
            url = make_query(ApplicantNumber, i)
            response = requests.get(url)
            data_dict = xmltodict.parse(response.content)
            
            try : 
                dict_list = data_dict['response']['body']['items']['item'] # 상표권 Dict list
            except : 
                print(idx, '실패(상표권 X)')
                continue
            
            if type(dict_list) == list :
                for DICT in dict_list : 
                    DICT['ID'] = ApplicantNumber 
                    db_trademark = db_trademark.append(DICT, ignore_index=1).reset_index(drop = 1)
            else : 
                dict_list['ID'] = ApplicantNumber 
                db_trademark = db_trademark.append(dict_list, ignore_index=1).reset_index(drop = 1)
                
    else : pass
    
    
    print(idx, '완료')
        
    # 전체 개수
    

    
db_trademark = db_trademark.drop_duplicates().reset_index(drop= 1)
db_trademark.to_csv(directory + '가전_상표권.csv', index= False , encoding='euc-kr')


#%% 5. 유사군 코드 추출 / API

def make_query(applicationNumber, pageNo = 1) :
    
    url_list = []
    url_list.append('http://plus.kipris.or.kr/openapi/rest/trademarkInfoSearchService/trademarkSimilarityCodeInfo') 
    
    url_list.append('?applicationNumber=')
    url_list.append(str(applicationNumber))
    
    key = 'PLkTuNb8ws1hTyHsOXZTrJX39gWk0wfexHpUyn5Q00E='
    url_list.append('&accessKey=')
    url_list.append(key)
    
    url = ''
    
    for i in url_list : url += i
    
    return(url)

db_trademark = pd.read_csv(directory + '가전_상표권.csv' , encoding='euc-kr')
db_trademark['SimilargroupCode'] = ''

for idx, row in db_trademark.iterrows() :
    
    applicationNumber = row['applicationNumber']
    
    url = make_query(applicationNumber)
    
    response = requests.get(url)
    data_dict = xmltodict.parse(response.content)
    
    try : 
        temp = data_dict['response']['body']['items']['trademarkSimilarityCodeInfo']
        temp = [i['SimilargroupCode'] for i in temp]
        db_trademark['SimilargroupCode'][idx] = '|'.join(temp)
        
    except :pass
    
    #%%
    
db_trademark.to_csv(directory + '가전_상표권.csv', index= False , encoding='euc-kr')
#%% 6. 유사군코드 조회

def make_query(similarCode, startNum = 1, endNum = 60) :
    
    url_list = []
    url_list.append('http://plus.kipris.or.kr/openapi/rest/trademarkInfoSearchService/trademarkSimilarCodeSearchInfo') 
    
    url_list.append('?similarCode=')
    url_list.append(str(similarCode))
    
    url_list.append('&startNum=')
    url_list.append(str(startNum))
    
    url_list.append('&EndNum=')
    url_list.append(str(endNum))
    
    key = 'PLkTuNb8ws1hTyHsOXZTrJX39gWk0wfexHpUyn5Q00E='
    url_list.append('&accessKey=')
    url_list.append(key)
    
    url = ''
    
    for i in url_list : url += i
    
    return(url)


#%%

#1. 유사군 코드 리스트 추출
total_SimilargroupCode_list = []


for idx, row in db_trademark.iterrows() :
    
    SimilargroupCode = row['SimilargroupCode']
    SimilargroupCode_list = SimilargroupCode.split('|')
    total_SimilargroupCode_list.append(SimilargroupCode_list)
    
total_SimilargroupCode_list = sum(total_SimilargroupCode_list ,[])
total_SimilargroupCode_list = list(set(total_SimilargroupCode_list))
total_SimilargroupCode_list.remove('')

#%%
#2. 유사군 코드 텍스트 추출
db_similarCode = {}
db_similarCodeEnglish = {}

for similarCode in total_SimilargroupCode_list :
    
    idx = 1
    df_similarCode = pd.DataFrame()
    
    # 끝까지 추출
    while(1) :
            
        url = make_query(similarCode, idx, idx+59)    
        response = requests.get(url)
        data_dict = xmltodict.parse(response.content)
    
        try : 
            temp = data_dict['response']['body']['items']['trademarkSimilarCodeSearchInfo']
            for DICT in temp :
                df_similarCode = df_similarCode.append(DICT, ignore_index=1).reset_index(drop = 1)
        except : break
    
        idx += 60

    try:
        asignProductName_set = set(df_similarCode['asignProductName'])
        asignProductNameEnglish_set = set(df_similarCode['asignProductNameEnglish'])
        db_similarCode[similarCode] = asignProductName_set
        db_similarCodeEnglish[similarCode] = asignProductNameEnglish_set
    except :
        db_similarCode[similarCode] =  None
        db_similarCodeEnglish[similarCode] = None
    

#%% 유사군 코드 저장
import pickle 

with open(directory + '유사군코드_국문.pkl', 'wb') as f :
    pickle.dump(db_similarCode, f)

with open(directory + '유사군코드_영문.pkl', 'wb') as f :
    pickle.dump(db_similarCodeEnglish, f)



#%% test
url_list = []
url_list.append('http://plus.kipris.or.kr/openapi/rest/CorpBsApplicantService/') 
url_list.append('corpBsApplicantInfoV2')

# url_list.append('?BusinessRegistrationNumber=')
# BusinessRegistrationNumber= '142-81-22888'
# url_list.append(BusinessRegistrationNumber)
# url_list.append('&accessKey=')
# url_list.append(key)

url_list.append('?CorporationNumber=')
CorporationNumber = '134511-0144268'
url_list.append(CorporationNumber)
url_list.append('&accessKey=')
url_list.append(key)


url = ''
for i in url_list : url += i

response = requests.get(url)

#%%


#%% 1. using API wrapper

import requests
from urllib.parse import urlencode, quote_plus
import xmltodict

# 상세 검색
url = 'http://plus.kipris.or.kr/kipo-api/kipi/trademarkInfoSearchService/getAdvancedSearch'

# applicant_list = []
count_list = []

for year in range(2010,2021) :
    year = str(year)
    ymd_st = year + '0101'
    ymd_ed = year + '1231'
    ymd = ymd_st + '~' + ymd_ed
    queryParams = '?' + urlencode({ quote_plus('ServiceKey') : '9Kw8B55gOr36nptCOyvrCEPcSpWdMweyGyzMYyJNe3KGovqAaCJRSQtbPNqdEMhG62tXL9eu0szpzYVwlQFwSg==',
                                # quote_plus('tradeMarkName') : '하늘사랑',
                               # quote_plus('classification') : '06',
                               # quote_plus('asignProduct') : '자동차*엔진*마개',
                               # quote_plus('applicationNumber') : '4020077000311',
                               # quote_plus('registerNumber') : '4007360880000',
                               # quote_plus('publicationNumber') : '4020070064074',
                               # quote_plus('internationalRegisterNumber') : '858125',
                               # quote_plus('priorityNumber') : '04329',
                                quote_plus('applicationDate') : ymd,
                                # quote_plus('registerDate') : '20090101~20090103',
                                # quote_plus('publicationDate') : '20100101~20101231',
                               # quote_plus('priorityDate') : '20090101~20090103',
                               # quote_plus('internationalRegisterDate') : '20090101~20090103',
                                quote_plus('applicantName') : '119980966899',
                               # quote_plus('agentName') : '특허법인*코리아나',
                               # quote_plus('viennaCode') : '010101',
                               # quote_plus('regPrivilegeName') : 'kim',
                               # quote_plus('freeSearch') : '30303',
                               # quote_plus('similarityCode') : 'G1004',
                               quote_plus('application') : 'true',
                               quote_plus('registration') : 'true',
                               quote_plus('refused') : 'true',
                               quote_plus('expiration') : 'true',
                               quote_plus('refused') : 'true',
                               quote_plus('expiration') : 'true',
                               quote_plus('withdrawal') : 'true',
                               quote_plus('publication') : 'true',
                               quote_plus('cancel') : 'true',
                               quote_plus('abandonment') : 'true',
                               quote_plus('trademark') : 'true', 
                               quote_plus('serviceMark') : 'true', 
                               quote_plus('trademarkServiceMark') : 'true', 
                               quote_plus('businessEmblem') : 'true', 
                               quote_plus('collectiveMark') : 'true', 
                               quote_plus('internationalMark') : 'true', 
                               quote_plus('character') : 'true', 
                                quote_plus('figure') : 'true', 
                               quote_plus('compositionCharacter') : 'true', 
                               quote_plus('figureComposition') : 'true' })
    
    response = requests.get(url + queryParams)
    data_dict = xmltodict.parse(response.content)
    
    temp = data_dict['response']['count']['totalCount']
    count_list.append(temp)
    # temp = data_dict['response']['body']['items']['item']
    # temp = [i['applicantName'] for i in temp]
    # temp = [i.split('|') for i in temp]
    # temp = sum(temp, [])
    # applicant_list.append(temp)
    print(year , " completed")
# queryParams = 

# c = data_dict[]

#%%

for year in range(2010,2021) :
    year = str(year)
    ymd_st = year + '0101'
    ymd_ed = year + '1231'
    ymd = ymd_st + '~' + ymd_ed
    queryParams = '?' + urlencode({ quote_plus('ServiceKey') : '9Kw8B55gOr36nptCOyvrCEPcSpWdMweyGyzMYyJNe3KGovqAaCJRSQtbPNqdEMhG62tXL9eu0szpzYVwlQFwSg==',
                                # quote_plus('tradeMarkName') : '하늘사랑',
                               # quote_plus('classification') : '06',
                               # quote_plus('asignProduct') : '자동차*엔진*마개',
                               # quote_plus('applicationNumber') : '4020077000311',
                               # quote_plus('registerNumber') : '4007360880000',
                               # quote_plus('publicationNumber') : '4020070064074',
                               # quote_plus('internationalRegisterNumber') : '858125',
                               # quote_plus('priorityNumber') : '04329',
                                quote_plus('applicationDate') : ymd,
                                # quote_plus('registerDate') : '20090101~20090103',
                                # quote_plus('publicationDate') : '20100101~20101231',
                               # quote_plus('priorityDate') : '20090101~20090103',
                               # quote_plus('internationalRegisterDate') : '20090101~20090103',
                                quote_plus('applicantName') : '119980966899',
                               # quote_plus('agentName') : '특허법인*코리아나',
                               # quote_plus('viennaCode') : '010101',
                               # quote_plus('regPrivilegeName') : 'kim',
                               # quote_plus('freeSearch') : '30303',
                               # quote_plus('similarityCode') : 'G1004',
                               quote_plus('application') : 'true',
                               quote_plus('registration') : 'true',
                               quote_plus('refused') : 'true',
                               quote_plus('expiration') : 'true',
                               quote_plus('refused') : 'true',
                               quote_plus('expiration') : 'true',
                               quote_plus('withdrawal') : 'true',
                               quote_plus('publication') : 'true',
                               quote_plus('cancel') : 'true',
                               quote_plus('abandonment') : 'true',
                               quote_plus('trademark') : 'true', 
                               quote_plus('serviceMark') : 'true', 
                               quote_plus('trademarkServiceMark') : 'true', 
                               quote_plus('businessEmblem') : 'true', 
                               quote_plus('collectiveMark') : 'true', 
                               quote_plus('internationalMark') : 'true', 
                               quote_plus('character') : 'true', 
                                quote_plus('figure') : 'true', 
                               quote_plus('compositionCharacter') : 'true', 
                               quote_plus('figureComposition') : 'true' })
    
    response = requests.get(url + queryParams)
    data_dict = xmltodict.parse(response.content)
    
    temp = data_dict['response']['count']['totalCount']
    count_list.append(temp)
    # temp = data_dict['response']['body']['items']['item']
    # temp = [i['applicantName'] for i in temp]
    # temp = [i.split('|') for i in temp]
    # temp = sum(temp, [])
    # applicant_list.append(temp)
    print(year , " completed")


#%% 2. using selenium for scraping freq

import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep


URL = 'http://www.kipris.or.kr/khome/main.jsp'

driver = webdriver.Chrome(executable_path='D:/OneDrive - 아주대학교/driver/chromedriver')
driver.get(url=URL)

# 클릭
path = '//*[@id="gnb"]/li[1]/div/ul/li[3]/a'
posting = driver.find_element_by_xpath(path)
posting.click()

trademark_cnt_dict = {}
# 전자
# kipris_id_list = [120090549631, 119980968279, 119981004741, 119980966899, 120150542187 ]
# 생활가전
# kipris_id_list = [120130293842,119990537571,119980007035,120170754514,119980031755 ]
# AV
# kipris_id_list = [120010161934,120010009907, 120010193959, 119980023344,119980006618 ]
# 조명
kipris_id_list = [119990239368, 120090012139, 119980027188, 120110084588, 119980039494]



for ID in kipris_id_list :
    ID = str(ID)
    # 검색어 입력
    driver.implicitly_wait(time_to_wait=3)
    path = '//*[@id="queryText"]'
    search_box = driver.find_element_by_xpath(path)
    
    cnt_list = []
    
    for year in range(2010,2021) :
        
        year = str(year)
        ymd_st = year + '0101'
        ymd_ed = year + '1231'
        ymd = ymd_st + '~' + ymd_ed
    
        query = 'AD=['+ymd+']*AP=['+ID+']'
        search_box.clear()
        search_box.send_keys(query)
        
        # 검색
        path = '//*[@id="SearchPara"]/fieldset/span[1]/a/img'
        posting = driver.find_element_by_xpath(path)
        posting.click()
        
        # 리턴
        try :
            path = '//*[@id="listForm"]/section/div[1]/p[2]/span[1]'
            posting = driver.find_element_by_xpath(path)        
            CNT = posting.text
            
        except : CNT = "0"
        
        cnt_list.append(CNT)
        print(year)
        
        # driver.implicitly_wait(time_to_wait=3)
        sleep(2)
        
    trademark_cnt_dict[ID] = cnt_list