import argparse, sys, os, django, re, urllib3, json, inspect, logging
import pandas as pd
import time 

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

from bs4 import BeautifulSoup
from django.core.files import File
from tempfile import NamedTemporaryFile
from scraper_functies import *


# Get root dir as a function of the current scripts containing dir (one level up)
root_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), '..'))
sys.path.append(root_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

# Supress urllib3 certificate warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class JobScraper:
    '''
    Web scraper class for different job websites
    '''

    # Constructor
    def __init__(self):
        
        # Public props
        self.scraper = ''
        self.show_output = False
        self.num_pages = -1 # -1 for high limit 10**8
        self.num_vacs = -1 # -1 for high limit 10**8
        self.start_page = 1
        self.logger = None


        # Protected properties
        self._scraper_urls = {
            'indeed': 'https://www.indeed.nl/jobs?q=data+scientist&l=nederland&start={}',
            }
            # 'jobbird': 'https://www.jobbird.com'

        # Private properties
        self.__http = urllib3.PoolManager()

    def scrape(self):

        if self.scraper:

            # To be able to break outer loop
            end_page = self.start_page + self.num_pages

            # Convert -1 values to ridiculously high values
            # so that scraper will scrape everything
            if self.num_pages == -1:
                end_page = self.start_page + 10**8
            if self.num_vacs == -1:
                self.num_vacs = 10**8

            for i in range(self.start_page, end_page):
                xrnd = np.random.uniform(3, 6)
                time.sleep(xrnd)
                # Get page according to page number
                page = self.__try_fetch_page(self._scraper_urls[self.scraper].format(i + 1))
                # Attempt to parse HTML output
                parsed_html =  BeautifulSoup(page, 'html.parser')

                # Get divs from parsed HTML
                divs = parsed_html.find_all(name="div", attrs={"class":"row"})

                if(len(divs) == 0):
                    break

                for div in divs:
                    scrape_data = dict()
                    scrape_data['titel'] = zoek_titel(div)
                    scrape_data['bedrijf'] = zoek_bedrijf(div)
                    scrape_data['plaats'] = zoek_locatie(div)
                    scrape_data['link'] = zoek_link(div)                    
                    vac_page = self.__try_fetch_page(self._scraper_urls[self.scraper].format(i + 1) + zoek_link(div))
                    parsed_html =  BeautifulSoup(vac_page, 'html.parser')
                    scrape_data['alles'] = zoek_alles(parsed_html)

##TODO:
# vanaf datum toevoegen
# log toevoegen

            return scrape_data

                        

