from django.urls import path
from . import views

urlpatterns = [
    path('map_popup/', views.map_popup, name='map_popup'),
    path('geocode_proxy/', views.geocode_proxy, name='geocode_proxy'),
]
