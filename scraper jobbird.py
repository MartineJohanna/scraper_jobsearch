#!/usr/bin/env python
# coding: utf-8

# In[2]:


# import packages
import requests
import pandas as pd
import numpy as np
import time 
import requests
import datetime
import pandas as pd
import re, html
import bs4
from bs4 import BeautifulSoup


# In[3]:


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)


# In[226]:


# functies voor de scraper

#get soup
def get_soup(text):
    return BeautifulSoup(text, "lxml", from_encoding="utf-8")

def zoek_divs(soup):
    divs = soup.find_all(name="a", attrs={'class':'job-result'})
    return divs

# zoek link van vacature
def zoek_link(div):
    return div['href']

# zoek locatie van de vacature
def zoek_plaats(div):
    places = div.find_all('span', 'job-result__place')
    for place in places:
        place = ''.join(place.get_text().split())[:-6]
        place = place.replace('(', '')
        return place

#zoek naam van bedrijf van de vacature
def zoek_bedrijven(div):
    bedrijven = div.find_all('span', 'dashed-list__item')
    for bedrijf in bedrijven:
        alles = []
        test = bedrijf.get_text()
        test = test.replace('Premium', '')
        test = test.replace('Nieuw', '')
        test = test.rstrip()
        alles.append(test)
        alles = ''.join(str(alles).split())[2:-4]
    return alles

#zoek inhoud gehele vacature
def hele_vac(soup):
    divs = soup.findAll("div",attrs={"class":"g-row-2"})
    text = []
    for div in divs:
        text.append(div.text.strip())
    return text

#zoek titel van de vacature
def zoek_titels(div):
    titles = div.find(name='h2', attrs={'class':"job-result__title"}).get_text()
    return titles

#zoek paginanummer van de vacature
def zoek_pagina(soup):
    pagina = soup.find(name='li', attrs={'class':'page-item active'}).get_text()
    pagina = int(pagina)
    return pagina


# In[227]:


titel=[]
bedrijf=[]
plaats=[]
link=[]

# scrapen van elke pagina

for i in range(1,1000):
    xrnd = np.random.uniform(3, 6)
    time.sleep(xrnd)
    
    page = requests.get('https://www.jobbird.com/nl/vacature?s=data%20scientist&p=Nederland&rad=alles&page='+ str(i) +'&ot=relevance')
    soup = get_soup(page.text)
    
    if(zoek_pagina(soup) < i):
        break
    
    divs = soup.find_all(name="a", attrs={'class':'job-result'})
    
    if(len(divs) == 0):
        break
        
        
    for div in divs:
        titel.append(zoek_titels(div))
        bedrijf.append(zoek_bedrijven(div))
        plaats.append(zoek_plaats(div))
        link.append(zoek_link(div))


# In[223]:


#dataframe van de resultaten
df = pd.DataFrame(
    {'titel': titel,
     'bedrijf': bedrijf,
     'plaats': plaats,
     'link': link
    })


# In[ ]:


# verwijderen van duplicates
df = df.drop_duplicates(subset='link', keep="first")


# In[230]:


# scrapen van de inhoud voor elke vacature
df2 = pd.DataFrame([])
vacs = []
cnt = -1
for _, vac in df.iterrows():   
    xrnd = np.random.uniform(3, 6)
    time.sleep(xrnd)
    
    num = (cnt + 1) 
    
    cnt = cnt + 1
#     if cnt > 10:
#         break;
        
    page = requests.get(vac['link'])
    soup = get_soup(page.text)
    alles = []
    
    alles.append(hele_vac(soup))
    df2[num] = alles
    
df2 = df2.T
df2.rename(columns={df2.columns[0]: "alles"}, inplace=True)
result = df.merge(df2, left_index=True, right_index=True)


# In[ ]:


df['plaats'] = df['plaats'].replace({'[^a-zA-Z]':' '},regex=True)
df['titel'] = df['titel'].replace({'[^a-zA-Z]':' '},regex=True)


# In[232]:


result.to_csv('jobbird_nederland.csv', encoding='utf-8', index=False)

