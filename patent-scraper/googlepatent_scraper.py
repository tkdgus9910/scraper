
import pandas as pd
from googlepatentscraper.document import Document

#%% 1. 경로설정 및 데이터 로드
directory = 'D:/github/IPR-scraper/uspto/' #수정

filename = 'gp-search-20211117-030702.csv' #수정
data = pd.read_csv(directory + filename,    skiprows=1)
#%%
patent = Document('US10003811').data

#%%

from google_patent_scraper import scraper_class

scraper=scraper_class()

patent_1 = 'US10003811'
# scraper.add_patents('US10003811')
# scraper.add_patents('US266827A')

err_1, soup_1, url_1 = scraper.request_single_patent(patent_1)

patent_1_parsed = scraper.get_scraped_data(soup_1,patent_1,url_1)

#%%
claims_list = [i['text'] for i in patent['claims']]
claims_text = claims_list[0]
for text in claims_list :
            claims_text += '\n\n' + text        
#%% 2. 특허번호 수정

id_list = data['id'].tolist()
id_list = [i[0:7]+'0'+i[7:] if i.startswith('US-20') else i for i in id_list]
id_list = [i[0:7]+'0'+i[7:] if i.startswith('US-19') else i for i in id_list]
id_list = [i.replace('-', '') for i in id_list]

#%% 3. 특허 텍스트 다운로드 및 저장

result_df = pd.DataFrame()

error_list = []

for idx, pt_id in enumerate(id_list) :
    
    print("전체 {} 중에서 {} 수집중".format(len(id_list),idx+1))
    
    try :
        DICT = {}
        patent = Document(pt_id).data
        claims_list = [i['text'] for i in patent['claims']]
        claims_text = ''
        
        cpc_list = patent['cpcs']
        cpc_list = [str(i['cpc']) for i in cpc_list]
        
        assignee_list = patent['assignee']
        assignee_list = [str(i) for i in assignee_list]
        
        date = patent['dates'][0]['date']   
        claims_text = "\n\n".join(claims_list)
            
        DICT['pt_id'] = pt_id
        DICT['date'] = date
        DICT['title'] = patent['title']
        DICT['abstract'] = patent['abstract']
        DICT['claims_rep'] = claims_list[0]
        DICT['claims'] = claims_text        
        DICT['description'] = patent['description_alt']
        DICT['cpc_list'] = cpc_list
        DICT['assignee_list'] = assignee_list
        DICT['assignee_list'] = assignee_list
            
        result_df = result_df.append(DICT, ignore_index=True)
    except : 
        error_list.append(pt_id)
        print('error pt_id is ' + pt_id )

result_df.to_csv(directory + 'pt_text.csv', index =0 )

#%%
import pickle 

with open(directory + 'DT_211118.pkl', 'wb') as fw:
    pickle.dump(result_df, fw)

#%%
    
patent = Document('US20210336857A1').data
cpc_list = patent['cpcs']
cpc_list = [str(i['cpc']) for i in cpc_list]

    