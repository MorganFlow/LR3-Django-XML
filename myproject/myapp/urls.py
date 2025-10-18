from django.urls import path
from . import views

urlpatterns = [
    path('', views.tour_list, name='home'),  # Стартовая страница — список туров
    path('add/', views.add_tour, name='add_tour'),
    path('upload/', views.upload_xml, name='upload_xml'),
    path('list/', views.tour_list, name='tour_list'),
]