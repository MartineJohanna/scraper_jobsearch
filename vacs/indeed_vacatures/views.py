from django.shortcuts import render
from django.http import JsonResponse
from .models import JobPost
from .scraper_indeed import scrape as execute_scrape
from django.db.models import Count

# Create your views here.

def index(request):
    job_posts = JobPost.objects.all()
    return render(request,'indeed_vacatures/index.html', {'jobPosts': job_posts})

def scrape(request):
    print('Ik begin nu')
    execute_scrape()
    return JsonResponse({"message": "gelukt"})


def pie_chart(request):
    labels = []
    data = []

        

        

    # queryset = JobPost.objects.all()

    queryset = JobPost.objects.values('plaats').order_by('plaats').annotate(count=Count('plaats'))
    for job in queryset:
        labels.append(job['plaats'])
        data.append(job['count'])


    return render(request, 'indeed_vacatures/pie_chart.html', {
        'labels': labels,
        'data': data,
    })



