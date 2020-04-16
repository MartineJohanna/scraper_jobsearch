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
import numpy as np
from bs4 import BeautifulSoup


# In[136]:


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)


# In[3]:


# get soup 
def get_soup(text):
    return BeautifulSoup(text, "lxml", from_encoding="utf-8")

#zoek titel van de functie
def zoek_titel(div):
        return div.find(name="acronym").get_text()

#zoek de locatie van de functie
def zoek_plaats(div):
    return div.find(attrs={'class':'padding'}).get_text()

#zoek link van de vacature
def zoek_link(div):
    link = ('https://www.it-contracts.nl' + div.find('a')['href'])
    return link

# zoek alle inhoud van de vacature
def zoek_alles(soup):
    return soup.find(name="div", attrs={"class":"vac-pagelayout"}).get_text()
    


# In[4]:


titel=[]
bedrijf=[]
plaats=[]
link=[]

# scrapen van elke pagina op zoekterm data scientist nederland

for i in range(1, 1000):
    xrnd = np.random.uniform(3, 6)
    time.sleep(xrnd)

    page = requests.get('https://www.it-contracts.nl/nieuwste-freelance-ict-opdrachten/search/data+scientist/from/'+ str(i))
    soup = get_soup(page.text)
    divs = soup.find_all(name="div", attrs={"class":"vacoverzicht-text"})
    
    if(len(divs) == 0):
        break

    for div in divs:
        
        titel.append(zoek_titel(div))
        plaats.append(zoek_plaats(div))
        link.append(zoek_link(div))


# In[5]:


# dataframe van de resultaten
df = pd.DataFrame(
    {'titel': titel,
     'plaats': plaats,
     'link': link
    })


# In[ ]:


# verwijderen van duplicates
df = df.drop_duplicates(subset='link', keep="first")


# In[7]:


# scrapen van de inhoud voor elke vacature
df2 = pd.DataFrame([])
cnt = -1
for _, vac in df.iterrows():   
    xrnd = np.random.uniform(3, 6)
    time.sleep(xrnd)
    
    num = (cnt + 1) 
    
    cnt = cnt + 1
        
    page =requests.get(vac['link'])
    soup = get_soup(page.text)
    alles = []
    
    alles.append(zoek_alles(soup))
    df2[num] = alles


# In[8]:


# joinen van de twee datasets
df2 = df2.T
df2.rename(columns={df2.columns[0]: "alles"}, inplace=True)
result = df.merge(df2, left_index=True, right_index=True)


# In[10]:


# opslaan van de resultaten
result.to_csv('it-contracts_nederland.csv', encoding='utf-8', index=False)

