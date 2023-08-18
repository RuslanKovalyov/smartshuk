from django.urls import path
from .views import honeypot_view

urlpatterns = [
    path('honeypot/', honeypot_view, name='honeypot'),
]
