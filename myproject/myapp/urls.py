from django.urls import path
from . import views

urlpatterns = [
    path('', views.tour_list, name='home'),
    path('add/', views.add_tour, name='add_tour'),
    path('upload/', views.upload_xml, name='upload_xml'),
    path('list/', views.tour_list, name='tour_list'),
    path('search/', views.ajax_search, name='ajax_search'),
    path('edit/<int:pk>/', views.edit_tour, name='edit_tour'),
    path('delete/<int:pk>/', views.delete_tour, name='delete_tour'),
]