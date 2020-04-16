#!/usr/bin/env python
# coding: utf-8

# In[1]:


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
import numpy as np
from bs4 import BeautifulSoup
from tqdm import tqdm


# In[2]:


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)


# In[2]:


# functies voor de scraper
def get_soup(text):
    return BeautifulSoup(text, "lxml", from_encoding="utf-8")

# titel van de functie
def zoek_titel(div):
    titel = div.find(attrs={'class':'title'})
    if titel is not None:
        return titel.get_text()

# bedrijf van de vacature    
def zoek_bedrijf(div):
    bedrijf = div.find('span', attrs={'class':'company'})
    if bedrijf is not None:
        return bedrijf.get_text()
    else: 
        sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
        return sec_try.get_text()

# locatie van de vacature
def zoek_locatie(div):
    locatie = div.find(attrs={'class':'location accessible-contrast-color-location'})
    if locatie is not None:
        return locatie.get_text()

# link naar de vacature
def zoek_link(div):
    for a in div.find_all(name='a', attrs={'data-tn-element':'jobTitle'}):
        return a['href']

# text van de vacature 
def zoek_alles(html):
    spans = soup.findAll('div', attrs={'class': "jobsearch-jobDescriptionText"})
    for span in spans:
        return span.text.strip()


# In[5]:


titel=[]
bedrijf=[]
plaats=[]
link=[]

# scrapen van elke pagina op zoekterm data engineering
for i in range(1, 1000):
    xrnd = np.random.uniform(3, 6)
    time.sleep(xrnd)

    page = requests.get('https://www.indeed.nl/jobs?q=data+engineer&l=nederland&start='+ str(i))
    soup = get_soup(page.text)
    divs = soup.find_all(name="div", attrs={"class":"row"})
    
    if(len(divs) == 0):
        break

    for div in divs:
        
        titel.append(zoek_titel(div))
        bedrijf.append(zoek_bedrijf(div))
        plaats.append(zoek_locatie(div))
        link.append(zoek_link(div))


# In[6]:


# dataframe van de resultaten
df = pd.DataFrame(
    {'titel': titel,
     'bedrijf': bedrijf,
     'plaats': plaats,
     'link': link
    })


# In[7]:


# verwijderen van duplicates
df = df.drop_duplicates(subset='link', keep="first")


# In[8]:


# scrapen van de inhoud voor elke vacature
df2 = pd.DataFrame([])
cnt = -1
for _, vac in df.iterrows():   
    xrnd = np.random.uniform(3, 4)
    time.sleep(xrnd)
    
    num = (cnt + 1) 
    
    cnt = cnt + 1
#     if cnt > 10:
#         break;
        
    page = requests.get('http://www.indeed.nl/' + vac['link'])
    soup = get_soup(page.text)
    alles = []
    
    alles.append(zoek_alles(soup))
    df2[num] = alles


# In[9]:


# joinen van de dataframes 
df2 = df2.T
df2.rename(columns={df2.columns[0]: "alles"}, inplace=True)
result = df.merge(df2, left_index=True, right_index=True)


# In[10]:


# dataframe opslaan
result.to_csv('indeed_nederland_engineering.csv', encoding='utf-8', index=False)

