from django.urls import path 
from . import views
from .views import export_scraper_csv
from .views import ScraperListView



urlpatterns =[
    path('', views.index, name = 'index'),
    path('scrape', views.scrape, name='scrape'),
    # path('pie-chart/', views.pie_chart, name='pie-chart'),
    path('export', export_scraper_csv, name='export_scraper_csv'),
    path("table/", ScraperListView.as_view())]
