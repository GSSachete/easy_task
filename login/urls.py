from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),  
    path('registrar/', views.register, name='register'), 
    path('logout/', views.logout, name='logout'),  
]