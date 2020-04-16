#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import packages
import requests
import pandas as pd
import numpy as np
import time 
import requests
import datetime
import pandas as pd
import re, html
import bs4
import json
from bs4 import BeautifulSoup


# In[10]:


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)


# In[2]:


# functies voor de scraper
def get_soup(text):
    return BeautifulSoup(text, "lxml", from_encoding="utf-8")

#zoek titel functie
def zoek_titel(divs):
    titel = div.find("h2",attrs={"class":"title"})
    if titel is not None:
        return titel.get_text()
    
#zoek link naar vacature
def zoek_link(divs):
    aa = div.find("a",attrs={"data-bypass":True})
    if aa is not None:
        return aa['href']

# zoek naam van bedrijf
def zoek_bedrijf(divs):
    comp = div.find("a",attrs={"class":"name"})
    if comp is not None:
        return comp.get_text()

# zoek locatie functie
def zoek_locatie(divs):
    locatie = div.find(attrs={"class":"location"})
    if locatie is not None:
        return locatie.get_text()

#zoek hele vacature    
def hele_vac(soup):
    vac = soup.find(attrs={'class':'job-description'})
    if vac is not None:
        return vac.get_text()
    
def laad_vac(soup):
    laad = soup.find(attrs={'id':'loadMoreJobs'})
    return laad.get_text()


# In[3]:


# scrapen van elke pagina op zoekterm data 
for i in range(1,1000):    
    
    titel=[]
    bedrijf=[]
    plaats=[]
    link=[]
    
    
    
    page = requests.get('https://www.monsterboard.nl/vacatures/zoeken/?q=data&where=nederland&cy=nl&stpage=1&page=' + str(i))
    soup = get_soup(page.text)
    divs = soup.findAll("div",attrs={"class":"flex-row"})
    
    if(len(divs) == 0):
        break
    
    for div in divs:
        titel.append(zoek_titel(div))
        bedrijf.append(zoek_bedrijf(div))
        plaats.append(zoek_locatie(div))
        link.append(zoek_link(div)) 
        
        if 'data' not in zoek_titel(div).lower():
            break



# In[6]:


# dataframe van de resultaten
df = pd.DataFrame(
    {'titel': titel,
     'bedrijf': bedrijf,
     'plaats': plaats,
     'link': link
    })


# In[12]:


# scrapen van de inhoud voor elke vacature
df2 = pd.DataFrame([])
vacs = []
cnt = 0
for _, vac in df.iterrows():   

    alles = []
    if vac['link'] is not None:
        xrnd = np.random.uniform(3, 6)
        time.sleep(xrnd)
        num = (cnt + 1)     
        cnt = cnt + 1
        
        
        original_url = vac['link']
        job_id = original_url.split('/')[-1]
        url = f'https://services.monster.io/jobs-svx-service/v1/jobs/{job_id}'
        r = requests.get(url)
        json_body = r.json()
        alles.append(json_body)
        df2[num] = alles


# In[8]:


# joinen van de dataframes 
df2 = df2.T
df2.rename(columns={df2.columns[0]: "alles"}, inplace=True)
result = df.merge(df2, left_index=True, right_index=True)


# In[50]:


# dataframe opslaan
result.to_csv('monsterboard_nederland.csv', encoding='utf-8', index=False)

