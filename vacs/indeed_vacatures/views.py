# packages
import csv
import time
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import ListView
from django_pandas.io import read_frame
from django_tables2 import SingleTableView
from plotly.graph_objs import Bar, Scatter
from plotly.offline import plot
from plotly.subplots import make_subplots
from .models import JobPost
from .scraper_indeed import scrape as execute_scrape
from .skills_vacatures import skills
from .tables import ScraperTable


# functie aanroepen van ScraperTable om een tabel te maken van de database
class ScraperListView(SingleTableView):
    model = JobPost
    table_class = ScraperTable
    template_name = 'indeed_vacatures/table.html'


# functie voor het scrapen van de vacaturesites
def scrape(request):

    print('Ik begin nu')
    execute_scrape()
    return JsonResponse({"message": "De site is nu gescraped"})

# functie voor het exporteren van de database naar csv bestand
def export_scraper_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="scraper_indeed.csv"'

    writer = csv.writer(response)
    writer.writerow( ['id', 'titel', 'bedrijf', 'plaats', 'zoekterm','alles', 'link', 'created_at', 'updated_at'])


    scraper_data = JobPost.objects.all().values_list('id', 'titel', 'bedrijf', 'plaats', 'zoekterm','alles', 'link', 'created_at', 'updated_at')
    for scrape in scraper_data:
        writer.writerow(scrape)
    return response



# functie voor creeeren van de dashboard
def index(request):

## ophalen en bewerken van de data uit de database 
# Query: tellen van aantal vacatures van data scientist en van data engineering
    labels_zoekterm = []
    data_zoekterm = []
    queryset_zoekterm = JobPost.objects.values('zoekterm').order_by('zoekterm').annotate(count=Count('zoekterm'))
    for term in queryset_zoekterm:
        labels_zoekterm.append(term['zoekterm'])
        data_zoekterm.append(term['count'])


# Query: tellen van aantal vacatures per bedrijf
    labels_bedrijf = []
    data_bedrijf = []
    queryset_bedrijf = JobPost.objects.values('bedrijf').order_by('bedrijf').annotate(count=Count('bedrijf'))
    for bedrijf in queryset_bedrijf:
        labels_bedrijf.append(bedrijf['bedrijf'])
        data_bedrijf.append(bedrijf['count'])

#Query: tellen van aantal vacatures per site
    labels_site = []
    data_site = []
    queryset_site = JobPost.objects.values('site').order_by('site').annotate(count=Count('site'))
    for s in queryset_site:
        labels_site.append(s['site'])
        data_site.append(s['count'])


#Query: tellen van aantal vacatures per plaats
    labels_plaats = []
    data_plaats = []
    queryset_plaats = JobPost.objects.values('plaats').order_by('plaats').annotate(count=Count('plaats'))
    for p in queryset_plaats:
        labels_plaats.append(p['plaats'])
        data_plaats.append(p['count'])

#Query: tellen van aantal vacatures per datum
    labels_date = []
    data_date = []
    queryset_date = JobPost.objects.values('updated_at').order_by('updated_at').annotate(count=Count('updated_at'))
    for dat in queryset_date:
        labels_date.append(dat['updated_at'])
        data_date.append(dat['count'])


#Query: skills die gezocht worden voor data scientist en data engineering
    filter_woorden = skills()

    keys_scientist = filter_woorden[0].keys()
    values_scientist = filter_woorden[0].values()

    
    keys_engineer = filter_woorden[1].keys()
    values_engineer = filter_woorden[1].values()

    
  # opzetten van de Dash dashboard
    app = dash.Dash()

# kleuren die gebruikt worden in de dashboard
    colors = {'background': '#111111', 'text': '#7FDBFF'}

# layout van de app
    app.layout = html.Div(style={'backgroundColor': colors['background']},children=[

        # barpolot van locaties
        dcc.Graph(
            id='Bar1',
            figure={
                'data': [
                    go.Bar(x=labels_plaats,
                    y=data_plaats,marker=dict(color='red')

                        
                    )
                ],
                'layout': go.Layout(
                    title = 'Locaties',
                    xaxis = {'title': 'locatie','categoryorder':'total descending'},
                    yaxis = {'title': 'aantal'},
                    hovermode='closest')}
        ),

        # barpolot van bedrijven
        dcc.Graph(
            id='Bar2',
            figure={
                'data': [
                    go.Bar(
                        x = labels_bedrijf,
                        y = data_bedrijf,
                        marker=dict(color='purple')
                        
                    )
                ],
                'layout': go.Layout(
                    title = 'Bedrijven',
                    xaxis = {'title': 'bedrijf','categoryorder':'total descending'},
                    yaxis = {'title': 'aantal'},
                    hovermode='closest')}
        ),
        # scatterplot van datums
        dcc.Graph(
            id='scat1',
            figure={
                'data': [
                    go.Scatter(
                        x = labels_date,
                        y = data_date,
                        marker=dict(color='purple')
                        
                    )
                ],
                'layout': go.Layout(
                    title = 'aantal vacatures',
                    xaxis = {'title': 'date'},
                    yaxis = {'title': 'aantal'},
                    hovermode='closest')}
        ),
# barplot van skills voor data engineering
        dcc.Graph(
            id='Bar3',
            figure={
                'data': [
                    go.Bar(
                        x=[k for k in keys_engineer],
                        y=[float(v) for v in values_engineer],
                        marker=dict(color='violet')
                        
                    )
                ],
                'layout': go.Layout(
                    title = 'Skills data engineering',
                    xaxis = {'title': 'skills'},
                    yaxis = {'title': 'aantal'},
                    hovermode='closest')}
        ),
# barplot van skills voor data scientist
        dcc.Graph(
            id='Bar4',
            figure={
                'data': [
                    go.Bar(
                        x=[k for k in keys_scientist],
                        y=[float(v) for v in values_scientist],
                        marker=dict(color='crimson')
                        
                    )
                ],
                'layout': go.Layout(
                    title = 'Skills data scientist',
                    xaxis = {'title': 'skills'},
                    yaxis = {'title': 'aantal'},
                    hovermode='closest')}
        ),

        
# piechart voor aantal vacatures per site
        dcc.Graph(id='pie',
                                figure={'data':[
                                    go.Pie(labels=labels_site, values=data_site

                                    )],
                                    'layout':go.Layout(title='site',
                                                        xaxis={'title': 'aantal'})}
                                    ),
# piechart voor aantal zoektermen 'data scientist' en 'data engineering' 
        dcc.Graph(id='pie2',
                            figure={'data':[
                                go.Pie(labels=labels_zoekterm, values=data_zoekterm
                                )],
                                'layout':go.Layout(title='zoektermen',
                                                    xaxis={'title': 'aantal'})}
        
    )])



    app.run_server(debug=True, use_reloader=False) 

    return render(request, "indeed_vacatures/index.html", context={'app': app})

