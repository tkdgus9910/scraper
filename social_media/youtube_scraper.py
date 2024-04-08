# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 14:58:50 2022

@author: tmlab
"""

if __name__ == '__main__':
    
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from oauth2client.tools import argparser
    import os
    
    # developer_key = os.environ.get('GOOGLE_API_KEY')
    # developer_key = 'AIzaSyDoUiom2fJ6YLdeZz20Rto8JPbhOaba2kw'
    developer_key = 'AIzaSyCd4kekzFDHMYGJxteS6H28meR7wWXXhWE'
    
    def build_youtube_search(developer_key):
      DEVELOPER_KEY = developer_key
      YOUTUBE_API_SERVICE_NAME="youtube"
      YOUTUBE_API_VERSION="v3"
      return build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)
  
    def get_search_response(youtube, query, year):
        search_response = youtube.search().list(
            q = query,
            order = "relevance",
            part = "snippet",
            regionCode = 'US', 
            maxResults = 50,
            publishedAfter= str(year) + '-01-01T00:00:00Z',
            publishedBefore= str(year) + '-12-31T23:59:59Z'
            ).execute()
        return search_response
  
    def get_search_response_token(youtube, query, pageToken, year):
        search_response = youtube.search().list(
            q = query,
            order = "relevance",
            part = "snippet",
            maxResults = 50,
            regionCode = 'US', 
            pageToken = pageToken,
            publishedAfter= str(year) + '-01-01T00:00:00Z',
            publishedBefore= str(year) + '-12-31T23:59:59Z'
            ).execute()
        return search_response
    
    
    def get_video_info(search_response):
      result_json = {}
      idx =0
      for item in search_response['items']:
        if item['id']['kind'] == 'youtube#video':
          result_json[idx] = info_to_dict(item['id']['videoId'], item['snippet']['title'], item['snippet']['description'], item['snippet']['thumbnails']['medium']['url'])
          idx += 1
      return 
  
    def info_to_dict(videoId, title, description, url):
      result = {
          "videoId": videoId,
          "title": title,
          "description": description,
          "url": url
      }
      return result
  
    #%%
    import pandas as pd
    import time
    
    search_query = ['samsung galaxy tablet', 'apple ipad tablet']
    # search_query = ['samsung galaxy tablet']
    
    youtube = build_youtube_search(developer_key)
    
    # result = pd.DataFrame()
    
    for year in range(2022, 2024) :
                
        for q in search_query : 
            # time.sleep(3)
            print(str(year) +'_' + q)
            
            # first res
            res = get_search_response(youtube, q, year)
            token = res['nextPageToken']
            items = res['items']
            items_ = []
            for i in items :
                i['query'] = q
                result = pd.concat([result, pd.DataFrame.from_dict(i ,orient = 'index').T] , axis = 0)
                # items_.append(i)
            
            # result = pd.concat([result, items_] , axis = 0)
            
            # second res
            max_page = 10
            stack = 1
            print(q + ' ' + str(stack))
            while(stack < max_page) :
                
                res = get_search_response_token(youtube, q, token, year)
                token = res['nextPageToken']
                items = res['items']
                items_ = []
                for i in items :
                    i['query'] = q
                    result = pd.concat([result, pd.DataFrame.from_dict(i ,orient = 'index').T] , axis = 0)
                    # items_.append(i)
                # result = result.append(items_, ignore_index= 1)
                stack +=1
                print(q + ' ' + str(stack))
    #%%
    
    
    temp = result.drop_duplicates(subset = ['id']).reset_index(drop = 1)
    #%%
    import numpy as np 
    result_after = pd.DataFrame()
    
    result_after['id'] = temp['id'].apply(lambda x : x['videoId'] if 'videoId' in x.keys() else np.NaN)
    
    result_after['publishedTime'] = temp['snippet'].apply(lambda x : x['publishedAt'])
    result_after['channelId'] = temp['snippet'].apply(lambda x : x['channelId'])
    result_after['description'] = temp['snippet'].apply(lambda x : x['description'])
    result_after['title'] = temp['snippet'].apply(lambda x : x['title'])
    result_after['query'] = temp['query']
    
    #%%
    directory = 'D:/OneDrive/data/BRM/youtube/'
    
    # result_after.to_csv(directory + 'youtube.csv')
    # result_after = pd.read_csv(directory + 'youtube.csv')
    result_after = result_after.loc[result_after['query'] == 'apple ipad tablet', : ]
    result_after['transcript_length'] = result_after['transcript'].apply(lambda x : len(x))
    # result_after['transcript_lentgh'] = result_after['transcript'].apply(lambda x : len(x))
    #%%
    result_after = result_after.loc[result_after['transcript_length'] >= 100, :].reset_index(drop= 1)
    
    #%% get transcript
    from youtube_transcript_api import YouTubeTranscriptApi
    
    developer_key = os.environ.get('GOOGLE_API_KEY')
    youtube = build('youtube','v3', developerKey= developer_key)
    
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

        # 자막 교체
        # for i in range(len(df)) : 
            
        #     temp = []
        #     full_script = df['transcript'][i]
            
        #     for item in full_script :
                
        #         temp.append(item['text'])
                
        #     df['transcript'][i] = " ".join(temp)
        
        return(df.reset_index(drop=True))
    
    scrapingTranscript(result_after, 'id')
    
    #%%
    
    result_after = result_after.loc[result_after['transcript'] != '',:].reset_index(drop = 1)
    result_after['transcript'] = result_after['transcript'].apply(lambda x : [i['text'] for i in x])
    
    #%%
    temp = result_after.drop_duplicates('transcript')
    #%%
    temp.to_csv(directory + 'youtube.csv', index = 0)