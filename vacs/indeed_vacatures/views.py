from django.shortcuts import render
from django.http import JsonResponse
from .models import JobPost
from .scraper_indeed import scrape as execute_scrape
from django.db.models import Count
from django.http import HttpResponse
import csv

# Create your views here.

def index(request):
    job_posts = JobPost.objects.all()
    return render(request,'indeed_vacatures/index.html', {'jobPosts': job_posts})

def scrape(request):
    print('Ik begin nu')
    execute_scrape()
    return JsonResponse({"message": "gelukt"})



def export_scraper_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="scraper_indeed.csv"'

    writer = csv.writer(response)
    writer.writerow(['alles', 'bedrijf', 'created_at', 'id', 'link', 'plaats', 'titel', 'updated_at', 'zoekterm'])

    scraper_data = JobPost.objects.all().values_list('alles', 'bedrijf', 'created_at', 'id', 'link', 'plaats', 'titel', 'updated_at', 'zoekterm')
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
