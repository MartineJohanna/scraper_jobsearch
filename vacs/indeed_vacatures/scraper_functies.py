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

    # titel van de functie
    def zoek_titel(self, div):
        titel = div.find(attrs={'class':'title'})
        if titel is not None:
            return titel.get_text()

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

    # link naar de vacature
    def zoek_link(self,div):
        for a in div.find_all(name='a', attrs={'data-tn-element':'jobTitle'}):
            link = 'https://www.indeed.nl/' + str(a['href'])
            return str(link)

    # text van de vacature 
    def zoek_alles(self,div):
        page = requests.get(self.zoek_link(div))
        page = page.text
        soup = BeautifulSoup(page, "lxml", from_encoding="utf-8")
        spans = soup.findAll('div', attrs={'class': "jobsearch-jobDescriptionText"})
        for span in spans:
            return span.text.strip()



class monsterboard:

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



    
