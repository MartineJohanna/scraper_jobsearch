from django.shortcuts import render
from .models import JobPost
from scraper_indeed import JobScraper

# Create your views here.

def index(request):
    job_posts = JobPost.objects.all()
    return render(request,'indeed_vacatures/index.html', {'job_posts': job_posts})

def create_from_dictionary(dict_vac):
    for job in dict_vac:
        job_post = JobPost(
            titel = job['titel'],
            bedrijf = job['bedrijf'],
            plaats = job['plaats'],
            link = job['link'],
            alles = job['alles'])
        job_post.save()
    return job_post

def scrape(request):
    dict_vac = scraper_indeed(request)
    create_from_dictionary(dict_vac=dict_vac)
    return render(request, 'indeed_vacatures/index.html', {'dict_vac': dict_vac})


def read(request):
    return 1

def delete(request):
    return 1