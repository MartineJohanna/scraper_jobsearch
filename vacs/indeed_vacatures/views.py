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




# Create your views here.

class ScraperListView(SingleTableView):
    model = JobPost
    table_class = ScraperTable
    template_name = 'indeed_vacatures/table.html'

def index(request):
    job_posts = JobPost.objects.all()
    aantal = JobPost.objects.all().count()
    return render(request,'indeed_vacatures/index.html', {'jobPosts': job_posts, 'aantal': aantal})

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


def pie_chart(request):
    labels = []
    data = []

    queryset = JobPost.objects.values('zoekterm').order_by('zoekterm').annotate(count=Count('zoekterm'))
    for job in queryset:
        labels.append(job['zoekterm'])
        data.append(job['count'])


    return render(request, 'indeed_vacatures/pie_chart.html', {
        'labels': labels,
        'data': data,
    })
