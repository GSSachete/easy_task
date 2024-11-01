from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


from django.shortcuts import render, redirect
from .models import Tarefa

@login_required
def menu(request):
    tarefas = Tarefa.objects.all()
    return render(request, 'menu/menu.html', {'tarefas': tarefas})
def adicionar_tarefa(request):
   
    return render(request, 'menu/adicionar_tarefa.html')