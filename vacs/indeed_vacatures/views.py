from django.shortcuts import render
from django.http import JsonResponse
from .models import JobPost
from .scraper_indeed import scrape as execute_scrape
from django.db.models import Count
from django.http import HttpResponse
import csv
import pandas as pd
from django_pandas.io import read_frame
from django.views.generic import ListView
from django_tables2 import SingleTableView
from .tables import ScraperTable
from plotly.offline import plot
from plotly.graph_objs import Scatter
from plotly.graph_objs import Bar
import plotly.io as pio
import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash
import dash_core_components as dcc
import dash_html_components as html
from plotly.subplots import make_subplots
import plotly
from .naar_coordinaten import coord
import numpy as np
import time
# from plotly import choropleth_mapbox



# Create your views here.

class ScraperListView(SingleTableView):
    model = JobPost
    table_class = ScraperTable
    template_name = 'indeed_vacatures/table.html'

# def index(request):
#     job_posts = JobPost.objects.all()
#     aantal = JobPost.objects.all().count()
#     return render(request,'indeed_vacatures/index.html', {'jobPosts': job_posts, 'aantal': aantal})

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


def index(request):

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




    
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{"type": "bar"}, {"type": "barpolar"}],
            [{"type": "pie"}, {"type": "scatter3d"}]],
    )

    fig.add_trace(go.Bar(x=labels_bedrijf,y=data_bedrijf),
                row=1, col=1)

    fig.add_trace(go.Barpolar(theta=[0, 45, 90], r=[2, 3, 1]),
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

    fig.add_trace(go.Scatter3d(x=[2, 3, 1], y=[0, 0, 0], 
                            z=[0.5, 1, 2], mode="lines"),
                row=2, col=2)

    fig.update_layout(height=1000, width=1000,
                  title_text="Scraper vacaturesites visualisaties")

    app = dash.Dash()
    app.layout = html.Div([
        dcc.Graph(figure=fig)
    ])

    app.run_server(debug=True, use_reloader=False) 

    return render(request, "indeed_vacatures/index.html", context={'app': app})


