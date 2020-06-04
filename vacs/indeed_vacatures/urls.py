from django.urls import path 
from . import views
from .views import export_scraper_csv
from .views import ScraperListView



urlpatterns =[
    path('', views.index, name = 'index'),
    path('dashboard/', views.dashboard, name ='django_plotly_dash'),
    path('scrape', views.scrape, name='scrape'),
    path('export', export_scraper_csv, name='export_scraper_csv'),
    path("table/", ScraperListView.as_view())]
