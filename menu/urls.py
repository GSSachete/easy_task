from django.urls import path
from . import views

urlpatterns = [
    path('inicio/', views.menu, name='menu'),
   
]