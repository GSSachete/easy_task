from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name='menu'), 
    path('adicionar_quadro/', views.adicionar_quadro, name='adicionar_quadro'), 
    path('editar_quadro/<int:quadro_id>/', views.editar_quadro, name='editar_quadro'),  
    path('excluir_quadro/<int:quadro_id>/', views.excluir_quadro, name='excluir_quadro'),
]
