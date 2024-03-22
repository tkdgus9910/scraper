# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 15:24:30 2022

@author: tmlab
"""


    
if __name__ == '__main__':
    
    import os
    import sys
    import re
    import pandas as pd
    import numpy as np     
    import pickle
    from datetime import datetime
    from datetime import timezone
    import pandas as pd
    from googlepatentscraper.document import Document

    directory = 'D:/SNU/TILAB - 문서/DB/Patent/Wisdomain/ev_hev_battery/'
    
    data = pd.read_csv(directory + 'CSV2208174828.csv',  skiprows=4)
    
    #%%        
    
    data['description'] = ''
    # text = Document(row['번호']).data['description_alt']
    except_list = []
    
    for idx, row in data.iterrows() :

        try :
            patent = Document(row['번호']).data
            data['description'][idx] = patent['description_alt']
            print(idx)
        except :
            except_list.append(idx)
            
            
    #%%            
    data.to_csv(directory + 'CSV2208174828_desc.csv', index = 0)
    
    
    #%%
    patent = Document('US20190354758A1').data
    # temp = data['description'][0]
    
    
    
        
        
        
    