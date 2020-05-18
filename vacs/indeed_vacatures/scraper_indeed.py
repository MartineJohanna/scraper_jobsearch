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
from indeed_vacatures.scraper_functies import indeed




def scrape():
    zoekterm = ['data+engineer', 'data+scientist']
    site = ['indeed']




    # scrapen van elke pagina op zoekterm data engineering
    for s in site:
        for j in zoekterm:
            for i in range(1, 2):

                if s == 'indeed':
                    scraper = indeed()
            


                xrnd = np.random.uniform(3, 6)
                time.sleep(xrnd)    

                soup = scraper.get_soup(page=scraper.get_page(i,j), i=i, j=j)
                divs = soup.find_all(name="div", attrs={"class":"row"})
                
                if(len(divs) == 0):
                    break

                test = []

                for div in divs:
                    scrape_data = dict()
                    scrape_data['titel'] = scraper.zoek_titel(div)
                    scrape_data['zoekterm'] = str(j)
                    scrape_data['bedrijf'] = scraper.zoek_bedrijf(div)
                    scrape_data['plaats'] = scraper.zoek_locatie(div)
                    scrape_data['link'] = scraper.zoek_link(div)
                    scrape_data['alles'] = scraper.zoek_alles(div)
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
                        
