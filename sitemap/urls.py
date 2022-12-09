from django.urls import path
from . import views

app_name = 'sitemap'

urlpatterns = [
    path('', views.map, name="map")

]