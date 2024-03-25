# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 15:21:45 2024

@author: tmlab
"""

import os
import praw # reddit library for scraping/crawler

reddit = praw.Reddit(client_id= 'QjnGy8LbLQDk_Q',
                     client_secret=os.environ.get('CLIENT_SECRET'),
                     password = 'asd35789',
                      user_agent='fakebot'
                     )

#%%
import time

# Create subreddit instance
subreddit = reddit.subreddit("GalaxyTab")

#%%
for submission in subreddit.hot(limit=25,   ):
    print(submission.title)
    
#%%
reddit = []

for submission in subreddit.top(time_filter="all"):
    reddit.append(submission)
    
    #%%
    submission.title # 제목
    submission.selftext # 본문
    submission.author # 저자
    submission.created_utc #시간

#%%