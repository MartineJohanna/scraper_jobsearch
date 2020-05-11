from django.shortcuts import render
from django.http import JsonResponse
from .models import JobPost
from .scraper_indeed import scrape as execute_scrape

# Create your views here.

def index(request):
    job_posts = JobPost.objects.all()
    return render(request,'indeed_vacatures/index.html', {'jobPosts': job_posts})

def scrape(request):
    print('Ik begin nu')
    execute_scrape()
    return JsonResponse({"message": "gelukt"})

