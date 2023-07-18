from django.urls import path, include
from . import views

urlpatterns = [
    path('real_estate/', views.real_estate, name="real_estate"),
    path('real_estate_post/', views.real_estate_post, name="real_estate_post"),
    path('real_estate_delete/<int:pk>/', views.real_estate_delete, name='real_estate_delete'),
    path('real_estate/<int:pk>/', views.real_estate_detail, name='real_estate_detail'),
    path('real_estate/liked_real_estate_ids_json/', views.liked_real_estate_ids_json, name='liked_real_estate_ids_json'),
    path('real_estate/like/<int:real_estate_id>/', views.real_estate_like, name='real_estate_like'),

    path('secondhand/', views.secondhand, name="secondhand"),
    path('secondhand_post/', views.secondhand_post, name="secondhand_post"),
    path('secondhand_delete/<int:pk>/', views.secondhand_delete, name='secondhand_delete'),
    path('secondhand/<int:pk>/', views.secondhand_detail, name='secondhand_detail'),
    path('secondhand/liked_secondhand_ids_json/', views.liked_secondhand_ids_json, name='liked_secondhand_ids_json'),
    path('secondhand/like/<int:secondhand_id>/', views.secondhand_like, name='secondhand_like'),

]