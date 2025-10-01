from django.urls import path
from .views import home
from . import views

urlpatterns = [
    path('', home, name='home'),
    path('add/', views.book_form, name='book_form'),
    path('books/', views.book_list, name='book_list'),

]