from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name='menu'),  # Página principal do menu
    path('adicionar_tarefa/', views.adicionar_tarefa, name='adicionar_tarefa'),  # Página de adicionar tarefa
]