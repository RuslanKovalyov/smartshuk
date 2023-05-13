from django.urls import path, include
from . import views

urlpatterns = [
    path('real_estate/', views.real_estate, name="real_estate"),
    path('real_estate_post/', views.real_estate_post, name="real_estate_post"),
    path('real_estate_delete/<int:pk>/', views.real_estate_delete, name='real_estate_delete'),
    path('real_estate/like/<int:real_estate_id>/', views.real_estate_like, name='real_estate_like'),
    path('real_estate/liked_real_estate_ids_json/', views.liked_real_estate_ids_json, name='liked_real_estate_ids_json'),
    path('real_estate/<int:pk>/', views.real_estate_detail, name='real_estate_detail'),

]