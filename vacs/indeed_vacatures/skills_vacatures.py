import collections
import re
import string
import xml.etree.ElementTree
from collections import Counter

# from nameparser.parser import HumanName
# import datefinder
import dash
import dash_core_components as dcc
import dash_html_components as html
import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
import plotly
import seaborn as sns
import spacy
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from plotly.subplots import make_subplots
from spacy import displacy

from .models import JobPost


def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def remove_punct(text):
    new_words = []
    for word in text:
        w = re.sub(r'[^\w\s]','',word) #remove everything except words and space#how 
                                        #to remove underscore as well
        w = re.sub(r'\_','',w)
        new_words.append(w)
    return new_words


def skills():

    vac_scientist_list = JobPost.objects.filter(zoekterm='data+scientist').values_list('alles', flat=True).order_by('pk')
    vac_scientist = JobPost.objects.filter(zoekterm='data+scientist')

    vac_scientist = str(vac_scientist.values('alles'))
    vac_engineer = str(JobPost.objects.filter(zoekterm='data+engineer').values('alles'))


    vac_scientist = remove_html_tags(vac_scientist).lower().split()
    vac_scientist = remove_punct(vac_scientist)

    vac_engineer = remove_html_tags(vac_engineer).lower().split()
    vac_engineer = remove_punct(vac_engineer)

    skills = ['python', 'r', 'ci/cd','ci', 'cd','py','mapr', 'spark', 'numpy', 'aws', 'google', 'nlp', 'stata',
            'regressie', 'multivariate', 'tableau', 'sql', 'nosql', 'nltk', 'ggplot', 'devops','linux',
            'docker', 'etl', 'mongodb', 'sas', 'mxnet', 'selenium', 'html', 'json', 'sqlite', 
            'sparkr', 'pytorch', 'theano', 'hadoop', 'mapreduce', 'angularjs', 'ubuntu', 'matplotlib',
            'qliksense', 'teano', 'github', 'pipelines', 'postgresql', 'css', 'corenlp', 'keras', 'fullstack',
            'spss', 'sparkml', 'spark','tensorflow', 'pandas', 'powerbi', 'css', 'openstack', 'php', 'cognos', 'bokeh',
            'redux', 'qlikview', 'newsql', 'sqladvanced', 'preprocessing', 'datavisualisatie', 'tableau', 'github',
            'gitlab', 'flask', 'azure', 'saas','mllib', 'redshift', 'opencv', 'bayesian', 'cassandra', 'nvidia', 'geopandas',
            'cloudera', 'clickview', 'spacy', 'frontend', 'backend', 'scikit', 'scikitlearn','scikit-learn', 'pyspark', 'mysql', 'arcgis',
            'spotfire', 'sqlalchemy', 'java', 'html', 'javascript', 'php', 'scala', 'hadoop', 'gis', 'shinyspark', 'svm',
            'wo', 'hbo', 'scipy', 'seaborn', 'statsmodels', 'julia', 'plotly', 'pydot', 'xgboost', 'lightgbm', 'catboost',
            'eli5', 'pytorch', 'gensim', 'scrapy', 'hive', 'pig', 'apache spark', 'kafka', 'django', 'mongodb', 'symphony', 'laravel',
            'postman', 'gatling', 'charles proxy', 'appnium', 'junit', 'selenium', 'webdriver', 'docker compose', 'kubernetes', 'terraform',
            'caffe', 'torch','splunk','hive', 'matlab', 'sas', 'ruby','perl',
            'postgressql', 'mysql', 'gunicorn', 'mysqllite', 'scala', 'git', 'bugsnag', 's3', ' ec2', 'ecs', 'rds', 'redshift', 'emr spark', 'ethena', 'glue']





    filter_scientist = []
    for i in vac_scientist:
        if i in skills:
            filter_scientist.append(i)
            
    top_skills_scientist = collections.Counter(filter_scientist).most_common(40)


    filter_engineer = []
    for i in vac_engineer:
        if i in skills:
            filter_engineer.append(i)
            
    top_skills_scientist = Counter(dict(collections.Counter(filter_scientist).most_common(40)))

    top_skills_engineer = Counter(dict(collections.Counter(filter_engineer).most_common(40)))



# collections.Counter(iets).most_common(10) 
    return top_skills_scientist, top_skills_engineer
