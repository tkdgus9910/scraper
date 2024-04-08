
import requests
import pandas as pd
from bs4 import BeautifulSoup

headers = {
    'authority': 'www.amazon.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9,bn;q=0.8',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    
}

cookie={} # insert request cookies within{}

headers = {
    'authority': 'www.amazon.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'accept-language': 'en-US,en;q=0.9',
    'sec-ch-ua': '"Chromium";v="104", "Google Chrome";v="104", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
}

cookies = {
    # Fill in with the cookies required for your session
    'session-id': '142-1234567-1234567', # Example cookie; replace with actual session cookie if needed
    # Add more cookies as necessary
}

headers = {
    'authority': 'www.amazon.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'accept-language': 'en-US,en;q=0.9',
    'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36 Edge/103.0.1264.49'
}

cookie = {} # insert request cookies within {}

#%%
def getAmazonSearch(search_query, page):
    page = str(page)
    url="https://www.amazon.com/s?k="+search_query+"&page="+page
    
    print(url)
    page=requests.get(url,headers=headers)
    
    if page.status_code==200:
        return page
    else:
        return "Error"
    
def Searchasin(asin):
    url="https://www.amazon.com/dp/"+asin
    print(url)
    page=requests.get(url,cookies=cookie,headers=headers)
    if page.status_code==200:
        return page
    else:
        return "Error"
     
def Searchreviews(review_link):
    url="https://www.amazon.com"+review_link
    print(url)
    page=requests.get(url,cookies=cookie,headers=headers)
    if page.status_code==200:
        return page
    
    else:
        return "Error"
    

#%% GET_ASIN test
# query = 'samsung+galaxy+tab'
query = 'apple+ipad'
data_asin_=[]

response=getAmazonSearch(query,3)
soup=BeautifulSoup(response.content)

# for i in soup.findAll("div",{'data-component-type':"s-search-result"}):
for i in soup.findAll("div",{'class':"sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16"}):
    
    # 광고 제외
    data_asin_.append(i['data-asin'])  
   
#%% 1-1. GET_ASIN iteration - 작동 잘 안됌
page = 1
data_asin=[]
query = 'apple+ipad'
# query = 'samsung+galaxy+tab'
while 1: 
    response=getAmazonSearch(query, page)
    asin = []
    soup=BeautifulSoup(response.content)
    for i in soup.findAll("div",{'class':"sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16"}):        
        # 광고 제외
        asin.append(i['data-asin'])  
    if len(asin) == 0 : break
    data_asin.append(asin)
    page +=1
    

data_asin = sum(data_asin, [])
#%% 1-2 asin data load
directory = 'D:/OneDrive/data/BRM/amazon/'
# data_asin = pd.read_csv(directory + 'asin_apple.csv', encoding = 'utf-8')
data_asin = pd.read_csv(directory + 'asin_samsung.csv', encoding = 'ISO-8859-1')
data_asin = list(data_asin['ASIN'])

#%% 2. scraping link and product names

asin2productName_dict = {}
asin2link_dict = {}

for i in range(0, len(data_asin)):
    
    response=Searchasin(data_asin[i])
    
    soup=BeautifulSoup(response.content)
    for j in soup.findAll("a",{'data-hook':"see-all-reviews-link-foot"}):
        
        if j['href'] in list(asin2link_dict.values()) : continue
        else : 
            asin2link_dict[data_asin[i]] = j['href']
        
    for j in soup.findAll("h1",{'id':"title"}):
        asin2productName_dict[data_asin[i]] = j.text.strip()
   
#%%

keys = list(asin2link_dict.keys())

# for key in keys :
#     if key not in 

   

#%% 3. scraping review

reviews = []

for asin in list(asin2link_dict.keys()) :
    link = asin2link_dict[asin]
    
    for k in range(1, 6): # 최대 50페이지가 한계
        temp = link + '&pageNumber=' + str(k) + '&sortBy=helpful'
        response = Searchreviews(temp)
        soup = BeautifulSoup(response.content)
        
        for i in soup.findAll("div", {'data-hook': "review"}):
            try:
                name = i.select_one('[class="a-profile-name"]').text.strip()
            except Exception as e:
                name = 'N/A'

            try:
                stars = i.select_one('[data-hook="review-star-rating"]').text.strip().split(' out')[0]
            except Exception as e:
                stars = 'N/A'   

            try:
                title = i.select_one('[data-hook="review-title"]').text.strip().split('\n')[1]
            except Exception as e:
                title = 'N/A'

            try:
                # Convert date str to dd/mm/yyy format
                date = i.select_one('[data-hook="review-date"]').text.strip().split(' on ')[-1]

            except Exception as e:
                date = 'N/A'

            try:
                description = i.select_one('[data-hook="review-body"]').text.strip()
            except Exception as e:
                description = 'N/A'
                
            try:
                verification = i.select_one('[data-hook="avp-badge"]').text.strip()
            except Exception as e:
                verification = 'N/A'
                
            # create Dictionary with all review data 
            data_dict = {
                'product_names': asin2productName_dict[asin],
                'ASIN': asin,
                'Name': name,
                'Stars': stars,
                'Title': title,
                'Date': date,
                'Verification': verification,
                'Description': description
            }

            # Add Dictionary in master empty List
            reviews.append(data_dict)
            
        if len(soup.findAll("div", {'data-hook': "review"})) < 10 : break
    #%%
    
    review_data=pd.DataFrame.from_dict(reviews)
    # pd.set_option('max_colwidth',800)
    #%%
    directory = 'D:/OneDrive/data/BRM/amazon/'
    review_data.to_csv(directory + 'samsung.csv')