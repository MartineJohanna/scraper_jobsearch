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





class indeed:
    

    # functies voor de scraper
    def get_page(self, i, j):
        page = requests.get('https://www.indeed.nl/jobs?q=' + j + '&l=nederland&start='+ str(i))
        page = page.text
        return page

    def get_soup(self, page, i, j):
        return BeautifulSoup(self.get_page(i,j), "lxml", from_encoding="utf-8")


    def get_divs(self,soup):
        divs = soup.find_all(name="div", attrs={"class":"row"})
        return divs

    # titel van de functie
    def zoek_titel(self, div):
        titel = div.find(attrs={'class':'title'})
        if titel is not None:
            return titel.get_text()
        else:
            return 'geen titel'

    # bedrijf van de vacature    
    def zoek_bedrijf(self,div):
        bedrijf = div.find('span', attrs={'class':'company'})
        if bedrijf is not None:
            return bedrijf.get_text()
        else: 
            sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
            return sec_try.get_text()

    # locatie van de vacature
    def zoek_locatie(self,div):
        locatie = div.find(attrs={'class':'location accessible-contrast-color-location'})
        if locatie is not None:
            return locatie.get_text()
        else:
            return 'geen locatie'

    # link naar de vacature
    def zoek_link(self,div):
        for a in div.find_all(name='a', attrs={'data-tn-element':'jobTitle'}):
            link = 'https://www.indeed.nl/' + str(a['href'])
            if link is not None:
                return str(link)
            else:
                return 'geen link'

    # text van de vacature 
    def zoek_alles(self,div):
        page = requests.get(self.zoek_link(div))
        page = page.text
        soup = BeautifulSoup(page, "lxml", from_encoding="utf-8")
        spans = soup.findAll('div', attrs={'class': "jobsearch-jobDescriptionText"})
        for span in spans:
            return span.text.strip()


class monsterboard:

    def get_page(self, i, j):
        page = requests.get('https://www.monsterboard.nl/vacatures/zoeken/?q=' + j +  '&where=nederland&stpage=' + str(1) + '&page=' + str(i + 1))
        page = page.text
        return page

    def get_soup(self, page, i, j):
        return BeautifulSoup(self.get_page(i,j), "lxml", from_encoding="utf-8")


    def get_divs(self,soup):
        divs = soup.findAll("div",attrs={"class":"flex-row"})
        return divs

    #zoek titel functie
    def zoek_titel(self,div):
        titel = div.find("h2",attrs={"class":"title"})
        if titel is not None:
            return titel.get_text()
        else:
            return "geen titel"

    # zoek naam van bedrijf
    def zoek_bedrijf(self,div):
        comp = div.find(attrs={"class":"company"})
        if comp is not None:
            return comp.get_text()
        else:
            return "geen bedrijf"


    # zoek locatie functie
    def zoek_locatie(self,div):
        locatie = div.find(attrs={"class":"location"})
        if locatie is not None:
            return locatie.get_text()
        else:
            return "geen locatie"
        
    #zoek link naar vacature
    def zoek_link(self, div):
        aa = div.find("a",attrs={"data-bypass":True})
        if aa is not None:
            return aa['href']
        else:
            return "geen link"

    def zoek_alles(self, div):
        original_url = self.zoek_link(div)
        job_id = original_url.split('/')[-1]
        url = f'https://services.monster.io/jobs-svx-service/v1/jobs/{job_id}'
        r = requests.get(url)
        json_body = r.json()
        if json_body is not None:
            return json_body
        else:
            return "geen vacature"



class jobbird:
    #get soup
    def get_page(self, i, j):
        if j == 'data+scientist':
            page = requests.get('https://www.jobbird.com/nl/vacature?s=data%20scientist&p=Nederland&rad=alles&page='+ str(i) +'&ot=relevance')
        else:
            page = requests.get('https://www.jobbird.com/nl/vacature?s=data%20engineer&p=Nederland&rad=alles&page='+ str(i) +'&ot=relevance')
        page = page.text
        return page

    def get_soup(self, page, i, j):
        return BeautifulSoup(self.get_page(i,j), "lxml", from_encoding="utf-8")

    def get_divs(self,soup):
        divs = soup.find_all(name="a", attrs={'class':'job-result'})
        return divs

    #zoek titel van de vacature
    def zoek_titel(self,div):
        titles = div.find(name='h2', attrs={'class':"job-result__title"}).get_text()
        if titles is not None:
            return titles
        else:
            return "geen titel"

    # zoek locatie van de vacature
    def zoek_locatie(self,div):
        places = div.find_all('span', 'job-result__place')
        loc = []
        if places is not None:
            for place in places:
                loc = ''.join(place.get_text().split())[:-6]
                loc = loc.replace('(', '')
                loc = " ".join(loc.split())
        else:
            loc = places
        return loc

    #zoek naam van bedrijf van de vacature
    def zoek_bedrijf(self,div):
        bedrijven = div.find_all('span', 'dashed-list__item')
        alles = []
        for bedrijf in bedrijven:
            test = bedrijf.get_text()
            test = test.replace('Premium', '')
            test = test.replace('Nieuw', '')
            test = test.rstrip()
            alles.append(test)
        alles = ''.join(str(alles).split())[7:-2]
        return alles


    # zoek link van vacature
    def zoek_link(self,div):
        link = div['href']
        if link is not None:
            return link
        else:
            return "geen link"

    #zoek inhoud gehele vacature
    def zoek_alles(self,div):
        page = requests.get(self.zoek_link(div))
        page = page.text
        soup = BeautifulSoup(page, "lxml", from_encoding="utf-8")
        divs = soup.findAll("div",attrs={"class":"g-row-2"})
        text = []
        for div in divs:
            text.append(div.text.strip())
        if text is not None:
            return text
        else:
            return "geen text"



