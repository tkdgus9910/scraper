# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 14:58:50 2022

@author: tmlab
"""

if __name__ == '__main__':
    
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from oauth2client.tools import argparser
    
    developer_key = "AIzaSyDawLbjbRP3Ac4vVJGbxKAIs0bnitdJKME" 
    
    def build_youtube_search(developer_key):
      DEVELOPER_KEY = developer_key
      YOUTUBE_API_SERVICE_NAME="youtube"
      YOUTUBE_API_VERSION="v3"
      return build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)
  
    def get_search_response(youtube, query):
        search_response = youtube.search().list(
            q = query,
            order = "relevance",
            part = "snippet",
            regionCode = 'US', 
            maxResults = 50,
            publishedAfter='2020-01-01T00:00:00Z',
            publishedBefore='2020-12-31T23:59:59Z'
            ).execute()
        return search_response
  
    def get_search_response_token(youtube, query, pageToken):
        search_response = youtube.search().list(
            q = query,
            order = "relevance",
            part = "snippet",
            maxResults = 50,
            regionCode = 'US', 
            pageToken = pageToken,
            publishedAfter='2020-01-01T00:00:00Z',
            publishedBefore='2020-12-31T23:59:59Z'
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
    
    search_query = ['samsung galaxy tab',
                     'apple ipad']
    
    youtube = build_youtube_search(developer_key)
    # res = get_search_response(youtube, 'apple ipad mini')
    # res = get_search_response(youtube, 'ipad', 'CDIQAA')
    
    result = pd.DataFrame()
    # search_query = ['samsung galaxy tab']
    
    for q in search_query : 
        
        # first res
        res = get_search_response(youtube, q)
        token = res['nextPageToken']
        items = res['items']
        items_ = []
        for i in items :
            i['query'] = q
            items_.append(i)
        result = result.append(items_, ignore_index= 1)
        
        # second res
        max_page = 10
        stack = 1
        print(q + ' ' + str(stack))
        while(stack < max_page) :
            
            res = get_search_response_token(youtube, q, token)
            token = res['nextPageToken']
            items = res['items']
            items_ = []
            for i in items :
                i['query'] = q
                items_.append(i)
            result = result.append(items_, ignore_index= 1)
            stack +=1
            print(q + ' ' + str(stack))
            
    #%%
    
    result_after = pd.DataFrame()
    
    result_after['id'] = result['id'].apply(lambda x : x['videoId'])
    result_after['publishedTime'] = result['snippet'].apply(lambda x : x['publishedAt'])
    result_after['channelId'] = result['snippet'].apply(lambda x : x['channelId'])
    result_after['description'] = result['snippet'].apply(lambda x : x['description'])
    result_after['title'] = result['snippet'].apply(lambda x : x['title'])
    result_after['query'] = result['query']
    directory = 'D:/OneDrive - SNU/db/BRM/youtube/'
    
    result_after.to_csv(directory + 'youtube.csv')
    
    #%% get transcript
    from youtube_transcript_api import YouTubeTranscriptApi
    
    #%%
    developer_key = "AIzaSyDawLbjbRP3Ac4vVJGbxKAIs0bnitdJKME" 
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
    
    
    scrapingTranscript(result_after, 'id')
    
    #%%
    
    result_after = result_after.loc[result_after['transcript'] != '',:].reset_index(drop = 1)
    temp = result_after.drop_duplicates('transcript')
    
    result_after.to_csv(directory + 'youtube.csv')