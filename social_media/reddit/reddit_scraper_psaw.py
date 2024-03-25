# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 15:21:45 2024

@author: tmlab
"""

import os
import praw # reddit library for scraping/crawler
from psaw import PushshiftAPI


r = praw.Reddit(    client_id= 'xYLb6kr4p4NCbQ45yRi2bw',
                     client_secret=os.environ.get('CLIENT_SECRET'),
                     username = 'tkdgus9910',
                     password = 'asd35789',
                     
                     user_agent='scrapingbot'
                     )

#%%

api = PushshiftAPI(r)

#%%

from psaw import PushshiftAPI

api = PushshiftAPI()