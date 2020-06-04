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
from .naar_coordinaten import coord
from .scraper_indeed import scrape as execute_scrape
from .skills_vacatures import skills
from .tables import ScraperTable

# from plotly import choropleth_mapbox



# Create your views here.

class ScraperListView(SingleTableView):
    model = JobPost
    table_class = ScraperTable
    template_name = 'indeed_vacatures/table.html'

def index(request):

    

    filter_woorden = skills()

    keys_scientist = filter_woorden[0].keys()
    values_scientist = filter_woorden[0].values()

    
    keys_engineer = filter_woorden[1].keys()
    values_engineer = filter_woorden[1].values()

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    app.layout = html.Div(children=[
        html.H1(children='Hello Dash'),

        html.Div(children='''
            Dash: A web application framework for Python.
        '''),

        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': [k for k in keys_scientist], 'y': [float(v) for v in values_scientist], 'type': 'bar', 'name': 'data scientist'},
                    {'x': [k for k in keys_engineer], 'y': [float(v) for v in values_engineer], 'type': 'bar', 'name': u'data engineer'},
                ],
                'layout': {
                    'title': 'Skills'
                }
            }
        )
    ])

    app.run_server(debug=True, use_reloader=False) 

    # aantal = JobPost.objects.all().count()
    return render(request, "indeed_vacatures/index.html", context={'app': app})

def scrape(request):

    print('Ik begin nu')
    execute_scrape()
    return JsonResponse({"message": "De site is nu gescraped"})


def export_scraper_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="scraper_indeed.csv"'

    writer = csv.writer(response)
    writer.writerow( ['id', 'titel', 'bedrijf', 'plaats', 'zoekterm','alles', 'link', 'created_at', 'updated_at'])


    scraper_data = JobPost.objects.all().values_list('id', 'titel', 'bedrijf', 'plaats', 'zoekterm','alles', 'link', 'created_at', 'updated_at')
    for scrape in scraper_data:
        writer.writerow(scrape)
    return response


# def pie_chart(request):
#     labels = []
#     data = []

#     queryset = JobPost.objects.values('zoekterm').order_by('zoekterm').annotate(count=Count('zoekterm'))
#     for job in queryset:
#         labels.append(job['zoekterm'])
#         data.append(job['count'])


#     return render(request, 'indeed_vacatures/pie_chart.html', {
#         'labels': labels,
#         'data': data,
#     })




# def index(request):
#     labels = []
#     data = []

#     queryset = JobPost.objects.values('bedrijf').order_by('bedrijf').annotate(count=Count('bedrijf'))
#     for job in queryset:
#         labels.append(job['bedrijf'])
#         data.append(job['count'])


#     fig = px.bar(y=data, x=labels)
#     plot_div = fig.show()

#     return render(request, "indeed_vacatures/index.html", context={'plot_div': plot_div})



# def pie_chart(request):
#     labels = []
#     data = []
#     queryset = JobPost.objects.values('zoekterm').order_by('zoekterm').annotate(count=Count('zoekterm'))
#     for job in queryset:
#         labels.append(job['zoekterm'])
#         data.append(job['count'])


#     fig = px.pie(values=data, names=labels)


    
#     app = dash.Dash()
#     app.layout = html.Div([
#         dcc.Graph(figure=fig)
#     ])

#     app.run_server(debug=True, use_reloader=False) 

#     return render(request, "indeed_vacatures/index.html", context={'app': app})


def dashboard(request):

    labels_zoekterm = []
    data_zoekterm = []
    queryset_zoekterm = JobPost.objects.values('zoekterm').order_by('zoekterm').annotate(count=Count('zoekterm'))
    for term in queryset_zoekterm:
        labels_zoekterm.append(term['zoekterm'])
        data_zoekterm.append(term['count'])

    labels_bedrijf = []
    data_bedrijf = []
    queryset_bedrijf = JobPost.objects.values('bedrijf').order_by('bedrijf').annotate(count=Count('bedrijf'))
    for bedrijf in queryset_bedrijf:
        labels_bedrijf.append(bedrijf['bedrijf'])
        data_bedrijf.append(bedrijf['count'])


    labels_site = []
    data_site = []
    queryset_site = JobPost.objects.values('site').order_by('site').annotate(count=Count('site'))
    for s in queryset_site:
        labels_site.append(s['site'])
        data_site.append(s['count'])


    labels_plaats = []
    data_plaats = []
    queryset_plaats = JobPost.objects.values('plaats').order_by('plaats').annotate(count=Count('plaats'))
    for p in queryset_plaats:
        labels_plaats.append(p['plaats'])
        data_plaats.append(p['count'])

    # lon_plaats = []
    # lat_plaats = []
    # labels_plaats=[]
    # data_plaats = []
    # queryset_plaats = JobPost.objects.values('plaats').order_by('plaats').annotate(count=Count('plaats'))
    # for plaats in queryset_plaats:
    #     xrnd = np.random.uniform(3, 6)
    #     time.sleep(xrnd)  
    #     labels_plaats.append(coord(plaats['plaats']))
    #     data_plaats.append(plaats['count'])

    #     latt = [x.strip() for x in labels_plaats[-1].split(',')][0]
    #     lon = latt = [x.strip() for x in labels_plaats[-1].split(',')][1]
    #     lon_plaats.append(lon)
    #     lat_plaats.append(latt)


    filter_woorden = skills()

    keys_scientist = filter_woorden[0].keys()
    values_scientist = filter_woorden[0].values()

    
    keys_engineer = filter_woorden[1].keys()
    values_engineer = filter_woorden[1].values()



    
    fig = make_subplots(
        rows=3, cols=2,
        specs=[[{"type": "bar"}, {"type": "pie"}],
            [{"type": "pie"}, {"type": "bar"}],
            [{"type": "bar"}, {"type": "bar"}]],
    )

    fig.add_trace(go.Bar(x=labels_bedrijf,y=data_bedrijf),
                row=1, col=1)

    fig.add_trace(go.Pie(labels=labels_site, values=data_site),
                row=1, col=2)

    # fig.add_trace(go.Figure(data=go.Scattergeo(
    #         lon = lon_plaats,
    #         lat = lat_plaats,
    #         mode = 'markers',
    #         marker_color = data_plaats,
    #         geo_scope='nl'
    #         )))

            

    fig.add_trace(go.Pie(labels=labels_zoekterm, values=data_zoekterm),
                row=2, col=1)

    fig.add_trace(go.Bar(x=labels_plaats,y=data_plaats),
                row=2, col=2).update_xaxes(categoryorder="total descending")

    
    fig.add_trace(go.Bar(x=[k for k in keys_engineer],y=[float(v) for v in values_engineer]),
                row=3, col=1).update_xaxes(categoryorder="total descending")


    fig.add_trace(go.Bar(x=[k for k in keys_scientist],y=[float(v) for v in values_scientist]),
                row=3, col=2).update_xaxes(categoryorder="total descending")


    fig.update_layout(height=2000, width=1700,
                  title_text="Scraper vacaturesites visualisaties")

    app = dash.Dash()
    app.layout = html.Div([
        dcc.Graph(figure=fig)
    ])

    app.run_server(debug=True, use_reloader=False) 

    return render(request, "indeed_vacatures/dashboard.html", context={'app': app})

