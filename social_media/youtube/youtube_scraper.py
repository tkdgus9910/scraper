
if __name__ == '__main__':

    # pip install youtube-search-python
    # pip install --upgrade google-api-python-client
    # pip install youtube_transcript_api
    from youtubesearchpython import VideosSearch
    from youtube_transcript_api import YouTubeTranscriptApi
    from bs4 import BeautifulSoup
    import pandas as pd
    import numpy as np
    import time
    import re
    import os 
    from datetime import datetime,timedelta
    from apiclient.discovery import build
    import requests

    #%% test
    from youtube_search import YoutubeSearch
    
    results = YoutubeSearch('samsung galaxy tab s', max_results=10,
                            ).to_dict()
    
    #%% 1. search url
    #'samsung galaxy tab s',
    search_query_ = [
                     'samsung galaxy tab a',
                     'samsung galaxy tab e',
                     'apple ipad mini',
                     'apple ipad air',
                     'apple ipad pro']
    
    for query in search_query_ :
    
        results = []
        search = VideosSearch(query, limit = 20, language = 'en',
                              region = 'US')
        i = 0
        
        while True : 
            temp = search.result()['result']    
            if len(temp) == 0 : break
            results.append(temp)
            search.next()
            i+=1
            print(i)
        
        results = sum(results , [])
        
        # 2. extract
        
        output = pd.DataFrame(columns = ['id','duration','publishedTime','title','viewCount'])
        
        for video in results :
            Id = video['id']
            Duration = video['duration']
            PublishedTime = video['publishedTime']
            Title = video['title']
            ViewCount = video['viewCount']['text']
            
            data= {'id' : Id,
                           'duration' : Duration,
                           'publishedTime' : PublishedTime,
                           'title' : Title,
                           'viewCount' : ViewCount}
          
            data = pd.DataFrame.from_records([data])
                                 
            output = pd.concat([output,data])
            
         
            # 3. save
        
            directory = 'D:/data/BRM/'
        
            output.to_csv(directory + query  + '.csv' , index= False)
    #%% 2. load & and subtitle extract
    
    api_key = "AIzaSyCUPU96nC4Oqzsg78O9PcKvVK3pvdVnieg" # 변경
    youtube = build('youtube','v3', developerKey= api_key)
    
    def scrapingTranscript(df, col) : 
        
    # =============================================================================
    # 자막 추출 함수
    # =============================================================================
        
        df = df
        col = col
        df['transcript'] = ''
        
        for i in range(len(df)) : 
            
            try : 
                df['transcript'][i] = YouTubeTranscriptApi.get_transcript(df[col][i])    
            
            except : pass
        
        # df = df[df['transcript'] != '']
        # df = df.reset_index(drop=True)
        
        # 자막 교체
        
        for i in range(len(df)) : 
            
            temp = []
            full_script = df['transcript'][i]
            
            for item in full_script :
                
                temp.append(item['text'])
                
            df['transcript'][i] = " ".join(temp)
            
        # df = df.drop_duplicates('transcript') # 중복제거(Id)     
        
        return(df.reset_index(drop=True))
    
    file_ = os.listdir(directory)
    
    for file in file_ :
        temp = pd.read_csv(directory + file)
        temp = scrapingTranscript(temp, 'id')
        temp.to_csv(directory + file,  index = False)