from django.urls import path
from . import views


app_name = 'main'

urlpatterns = [
    path('', views.map, name='map'),


    path("data/", views.data, name="data"),
    path('download_file/<str:filename>/', views.download_file, name="download_file"),
]