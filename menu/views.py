from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Tarefa
from .forms import TarefaForm


from django.shortcuts import render, redirect
from .models import Tarefa

@login_required
def menu(request):
    # Define a ordem de prioridade
    prioridade_ordem = {'urgente': 1, 'proximo': 2, 'distante': 3}
    
    # Ordena os quadros com base na prioridade
    quadros = Tarefa.objects.filter(usuario=request.user).all()
    quadros = sorted(quadros, key=lambda x: prioridade_ordem.get(x.prioridade, 4))
    
    return render(request, 'menu/menu.html', {'quadros': quadros})




from django.shortcuts import render, redirect
from .models import Tarefa
from .forms import TarefaForm
from django.contrib.auth.decorators import login_required

@login_required
def adicionar_quadro(request):
    if request.method == 'POST':
        form = TarefaForm(request.POST)
        if form.is_valid():
            tarefa = form.save(commit=False)
            tarefa.usuario = request.user  # Associa a tarefa ao usuário logado
            tarefa.save()
            return redirect('menu')  # Redireciona para o menu após salvar
    else:
        form = TarefaForm()
    return render(request, 'menu/adicionar_quadro.html', {'form': form})





@login_required
def editar_quadro(request, quadro_id):
    quadro = get_object_or_404(Tarefa, id=quadro_id, usuario=request.user)  # Garante que o quadro pertence ao usuário

    if request.method == 'POST':
        form = TarefaForm(request.POST, instance=quadro)
        if form.is_valid():
            form.save()
            return redirect('menu')  # Redireciona para o menu após salvar
    else:
        form = TarefaForm(instance=quadro)

    return render(request, 'menu/editar_quadro.html', {'form': form, 'quadro': quadro})


@login_required
def excluir_quadro(request, quadro_id):
    quadro = get_object_or_404(Tarefa, id=quadro_id, usuario=request.user)  # Verifica que o quadro pertence ao usuário
    quadro.delete()
    messages.success(request, 'Tarefa concluída e excluída com sucesso.')  # Mensagem de confirmação
    return redirect('menu')