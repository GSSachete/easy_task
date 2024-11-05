from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Tarefa
from .forms import TarefaForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Tarefa
from login.models import Usuario


@login_required
def menu(request):
    prioridade_ordem = {'urgente': 1, 'proximo': 2, 'distante': 3}
    
    quadros = Tarefa.objects.filter(usuario=request.user, concluida=False).all()
    quadros = sorted(quadros, key=lambda x: prioridade_ordem.get(x.prioridade, 4))
    
    return render(request, 'menu/menu.html', {'quadros': quadros})




@login_required
def adicionar_quadro(request):
    if request.method == 'POST':
        form = TarefaForm(request.POST)
        if form.is_valid():
            tarefa = form.save(commit=False)
            tarefa.usuario = request.user  
            tarefa.save()  

            nomes_usuarios = form.cleaned_data.get('participantes')
            if nomes_usuarios:
                nomes_usuarios = [nome.strip() for nome in nomes_usuarios.split(",")]
                for nome in nomes_usuarios:
                    try:
                        usuario = Usuario.objects.get(usuario=nome)
                        tarefa.participantes.add(usuario)
                    except Usuario.DoesNotExist:
                        pass
            
            return redirect('menu')  
    else:
        form = TarefaForm()
    return render(request, 'menu/adicionar_quadro.html', {'form': form})




@login_required
def editar_quadro(request, quadro_id):
    quadro = get_object_or_404(Tarefa, id=quadro_id, usuario=request.user)  

    if request.method == 'POST':
        form = TarefaForm(request.POST, instance=quadro)
        if form.is_valid():
            quadro = form.save(commit=False)  
            quadro.save()

            nomes_usuarios = form.cleaned_data.get('participantes')
            if nomes_usuarios:
                nomes_usuarios = [nome.strip() for nome in nomes_usuarios.split(',')]
                
                participantes = []
                for nome in nomes_usuarios:
                    try:
                        usuario = Usuario.objects.get(usuario=nome) 
                        participantes.append(usuario)
                    except Usuario.DoesNotExist:
                        pass
                
                quadro.participantes.set(participantes)  
            else:
                quadro.participantes.clear()  
            
            return redirect('menu')  
    else:
        nomes_existentes = ', '.join([user.usuario for user in quadro.participantes.all()])
        form = TarefaForm(instance=quadro, initial={'participantes': nomes_existentes})

    return render(request, 'menu/editar_quadro.html', {'form': form, 'quadro': quadro})


@login_required
def excluir_quadro(request, quadro_id):
    quadro = get_object_or_404(Tarefa, id=quadro_id, usuario=request.user)  
    quadro.delete()
    messages.success(request, 'Tarefa concluída e excluída com sucesso.')  
    return redirect('menu')

@login_required
def concluidos(request):
    usuario_instancia = Usuario.objects.get(user=request.user)

    tarefas_concluidas = Tarefa.objects.filter(
        concluida=True,
        usuario=request.user  
    ) | Tarefa.objects.filter(
        concluida=True,
        participantes=usuario_instancia  
    )

    tarefas_concluidas = tarefas_concluidas.distinct()

    return render(request, 'menu/concluidos.html', {'tarefas_concluidas': tarefas_concluidas})


@login_required
def concluir_tarefa(request, quadro_id):
    tarefa = Tarefa.objects.get(id=quadro_id, usuario=request.user)
    tarefa.concluida = True
    tarefa.save()
    return redirect('menu')
 
@login_required
def adicionar_participante(tarefa, nome_usuario):
    usuario = get_object_or_404(User, usuario=nome_usuario)
    tarefa.participantes.add(usuario)
    tarefa.save()

@login_required
def tarefas_em_grupo(request):
    usuario = request.user

    tarefas_em_grupo = Tarefa.objects.filter(
        participantes__user=usuario,
        concluida=False
    ) | Tarefa.objects.filter(
        usuario=usuario,
        participantes__isnull=False,
        concluida=False
    )

    tarefas_em_grupo = tarefas_em_grupo.distinct()

    return render(request, 'menu/tarefas_em_grupo.html', {'tarefas': tarefas_em_grupo})
