# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 15:21:45 2024

@author: tmlab
"""

import os
import praw # reddit library for scraping/crawler
from psaw import PushshiftAPI


r = praw.Reddit(client_id= 'QjnGy8LbLQDk_Q',
                     client_secret=os.environ.get('CLIENT_SECRET'),
                     password = 'asd35789',
                     
                      user_agent='fakebot'
                     )


api = PushshiftAPI(r)

#%%