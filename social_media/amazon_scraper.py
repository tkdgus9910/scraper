
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


#%%
search_query="nike+shoes+men"
base_url="https://www.amazon.com/s?k="
url=base_url+search_query
print(url)

#%%
search_response=requests.get(url,headers=headers)

#%%
search_response.status_code
cookie={} # insert request cookies within{}

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
    
  #%% GET_Product name

product_names=[]
# response=getAmazonSearch('nike+shoes+men')
response=getAmazonSearch('samsung+galaxy+tab')
soup=BeautifulSoup(response.content)

for i in soup.findAll("span",{'class':'a-size-medium a-color-base a-text-normal'}): # the tag which is common for all the names of products
    # 광고도 포함
    product_names.append(i.text) 
    
 #%% GET_ASIN
 
data_asin=[]
# response=getAmazonSearch('nike+shoes+men')
response=getAmazonSearch('samsung+galaxy+tab',3)

soup=BeautifulSoup(response.content)
# for i in soup.findAll("div",{'data-component-type':"s-search-result"}):
for i in soup.findAll("div",{'class':"sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16"}):
    
    # 광고 제외
    data_asin.append(i['data-asin'])  
    
#%% GET_ASIN iteration
page = 1
data_asin=[]

while 1: 
    
    query = 'samsung+galaxy+tab'
    response=getAmazonSearch('samsung+galaxy+tab', page)
    asin = []
    soup=BeautifulSoup(response.content)
    # for i in soup.findAll("div",{'data-component-type':"s-search-result"}):
    for i in soup.findAll("div",{'class':"sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16"}):
        
        # 광고 제외
        asin.append(i['data-asin'])  
    
    
    if len(asin) == 0 : break
    data_asin.append(asin)
    page +=1
    

data_asin = sum(data_asin, [])
   
#%% scraping link
link=[]

for i in range(len(data_asin)):
    response=Searchasin(data_asin[i])
    soup=BeautifulSoup(response.content)
    for i in soup.findAll("a",{'data-hook':"see-all-reviews-link-foot"}):
        link.append(i['href'])
        
#%%
reviews = []
for j in range(len(link)):
    for k in range(10):
        response = Searchreviews(link[j] + '&pageNumber=' + str(k))
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
                'product':product_names[j],
                'Name': name,
                'Stars': stars,
                'Title': title,
                'Date': date,
                'Verification': verification,
                'Description': description
            }

            # Add Dictionary in master empty List
            reviews.append(data_dict)
            
    #%%
    
    review_data=pd.DataFrame.from_dict(reviews)
    # pd.set_option('max_colwidth',800)
    
    directory = 
    review_data.to_csv('Scraping reviews.csv')