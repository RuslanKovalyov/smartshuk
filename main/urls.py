from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('terms/', views.policy, name='policy'),
    path('about/', views.about, name='about'),
]