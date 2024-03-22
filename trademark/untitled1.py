# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 16:56:14 2023

@author: tmlab
"""

import pandas as pd
import requests
from urllib.parse import urlencode, quote_plus
import xmltodict

key = 'PLkTuNb8ws1hTyHsOXZTrJX39gWk0wfexHpUyn5Q00E='

url = 'http://plus.kipris.or.kr/openapi/rest/ForeignPatentBibliographicService/bibliographicInfo?literatureNumber=000005640865A1&countryCode=US&accessKey='

url += key

response = requests.get(url)
data_dict = xmltodict.parse(response.content)


#%%


def make_query(ApplicantNumber, pageNo = 1) :
    
    url_list = []
    url_list.append('http://plus.kipris.or.kr/kipo-api/kipi/patUtiModInfoSearchSevice/') 
    
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