from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('menu/', views.menu, name='menu'),
    path('logout/', views.logout, name='logout'),
]