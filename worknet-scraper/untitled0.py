# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 09:16:09 2022

@author: tmlab
"""

if __name__ == '__main__':
    
    import os
    import sys
    import pandas as pd
    import numpy as np
    import requests
    import json
    import xmltodict
    
    key = 'WNL65PY1H25D7X9KZVHZD2VR1HK'
    
    # query = '&callTp=L&returnType=XML&startPage=200&display=100&sortOrderBy=ASC' # 채용정보
    # url = 'http://openapi.work.go.kr/opi/opi/opia/wantedApi.do?authKey=' + key + query

    
    # query = '&callTp=L&returnType=XML&startPage=1&display=10'
    # url = 'http://openapi.work.go.kr/opi/opi/opia/dhsOpenEmpInfoAPI.do?authKey=' + key + query # 공채속보 x
    
    query = '&callTp=L&returnType=XML&startPage=1&display=100&srchBgnDt=2000-01-01&srchEndDt=2001-12-31'
    url = 'http://openapi.work.go.kr/opi/opi/opia/empEventApi.do?authKey=' + key + query # 채용행사
    
    
    
    res = requests.get(url)
    
    text = res.text
    
    dict_type = xmltodict.parse(res.text)
    json_type = json.dumps(dict_type)
    dict2_type = json.loads(json_type)
    
    
    # temp = root[0]
    
    # print(text)
    
    # json_ob = json.loads(text)