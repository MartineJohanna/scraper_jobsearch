#!/usr/bin/env python
# coding: utf-8

# import packages
import requests
# import pandas as pd                  
import numpy as np
import time 
import requests
import datetime
import re, html
import bs4
from bs4 import BeautifulSoup
from indeed_vacatures.models import JobPost
from indeed_vacatures.scraper_functies import *




def scrape():
    zoekterm = ['data+engineer', 'data+scientist']


    # scrapen van elke pagina op zoekterm data engineering
    for j in zoekterm:
        for i in range(1, 2):
            xrnd = np.random.uniform(3, 6)
            time.sleep(xrnd)    

            page = requests.get('https://www.indeed.nl/jobs?q=' + j + '&l=nederland&start='+ str(i))
            soup = get_soup(page.text)
            divs = soup.find_all(name="div", attrs={"class":"row"})
            
            if(len(divs) == 0):
                break

            test = []

            for div in divs:
                print(div)
                scrape_data = dict()
                scrape_data['titel'] = zoek_titel(div)
                scrape_data['zoekterm'] = str(j)
                scrape_data['bedrijf'] = zoek_bedrijf(div)
                scrape_data['plaats'] = zoek_locatie(div)
                scrape_data['link'] = ('https://www.indeed.nl/' + str(zoek_link(div)))
                page = requests.get('http://www.indeed.nl/' + zoek_link(div))
                soup = get_soup(page.text)
                scrape_data['alles'] = zoek_alles(soup)
                test.append(scrape_data)

            for job in test:
                print("Saving" + job['titel'])
                job_post = JobPost(
                    titel = job['titel'],
                    zoekterm = job['zoekterm'],
                    bedrijf = job['bedrijf'],
                    plaats = job['plaats'],
                    link = job['link'],
                    alles = job['alles'])
                job_post.save()
                    
