from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name='menu'), 
    path('adicionar_quadro/', views.adicionar_quadro, name='adicionar_quadro'), 
    path('editar_quadro/<int:quadro_id>/', views.editar_quadro, name='editar_quadro'),  
    path('excluir_quadro/<int:quadro_id>/', views.excluir_quadro, name='excluir_quadro'),
    path('concluir_tarefa/<int:quadro_id>/', views.concluir_tarefa, name='concluir_tarefa'),
    path('concluidos/', views.concluidos, name='concluidos'),
    path('tarefas_em_grupo/', views.tarefas_em_grupo, name='tarefas_em_grupo'),
]
