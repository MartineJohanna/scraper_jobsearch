
import json
import requests as r
import numpy as np
import time

def coord(plaats):
    xrnd = np.random.uniform(3, 6)
    time.sleep(xrnd)  
    url = "https://geocode.xyz/"+plaats.replace(" ", "+")+"?json=1"
    response = r.get(url)
    json = response.json()
    coordinaten = str(json['latt']) + ',' + str(json['longt'])
    return coordinaten