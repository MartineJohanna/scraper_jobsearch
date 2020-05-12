from django.urls import path 
from . import views


urlpatterns =[
    path('', views.index, name = 'index'),
    path('scrape', views.scrape, name='scrape'),
    path('pie-chart/', views.pie_chart, name='pie-chart')
    
]
