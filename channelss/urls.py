from django.urls import path
from . import views

urlpatterns = [
    path('', views.room_list, name='room_list'),  # Lista de salas de chat
    path('chat/<str:room_name>/', views.chat_room, name='chat_room'),  # Sala de chat específica
]