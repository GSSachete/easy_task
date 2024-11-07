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
from .models import Message



@login_required
def menu(request):
    prioridade_ordem = {'urgente': 1, 'proximo': 2, 'distante': 3}
    quadros = Tarefa.objects.filter(usuario=request.user, concluida=False).all()
    quadros = sorted(quadros, key=lambda x: prioridade_ordem.get(x.prioridade, 4))
    
    users = User.objects.exclude(id=request.user.id)  
    
    return render(request, 'menu/menu.html', {'quadros': quadros, 'users': users})




@login_required
def adicionar_quadro(request):
    if request.method == 'POST':
        form = TarefaForm(request.POST, request.FILES)  # Inclua request.FILES para lidar com arquivos
        if form.is_valid():
            tarefa = form.save(commit=False)
            tarefa.usuario = request.user  
            tarefa.save()

            # Salva os arquivos se houver algum (supondo que o campo seja um FileField ou ImageField diretamente em Tarefa)
            if request.FILES.get('arquivo'):
                tarefa.arquivo = request.FILES.get('arquivo')  # Atribua o arquivo diretamente ao campo
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
        form = TarefaForm(request.POST, request.FILES, instance=quadro)
        if form.is_valid():
            quadro = form.save(commit=False)  

            # Substitui o arquivo existente se um novo for enviado
            if request.FILES.get('arquivo'):
                quadro.arquivo = request.FILES.get('arquivo')  # Substitui ou atribui diretamente o arquivo
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
    # Tenta obter a instância de Usuario associada ao usuário logado
    try:
        usuario_instancia = Usuario.objects.get(user=request.user)
    except Usuario.DoesNotExist:
        messages.error(request, "Você não possui um perfil de usuário registrado.")
        return redirect('menu')

    # Filtra as tarefas concluídas onde o usuário logado (request.user) é o criador
    # ou onde o usuario_instancia está nos participantes
    tarefas_concluidas = Tarefa.objects.filter(
        concluida=True,
        usuario=request.user  # Usa request.user (instância de User)
    ) | Tarefa.objects.filter(
        concluida=True,
        participantes=usuario_instancia  # Usa usuario_instancia (instância de Usuario)
    )

    # Remove duplicatas caso o usuário seja tanto criador quanto participante
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

    # Obtém as tarefas em grupo relacionadas ao usuário
    tarefas_em_grupo = Tarefa.objects.filter(
        participantes__user=usuario,
        concluida=False
    ) | Tarefa.objects.filter(
        usuario=usuario,
        participantes__isnull=False,
        concluida=False
    )
    tarefas_em_grupo = tarefas_em_grupo.distinct()

    # Filtra as pessoas envolvidas em cada tarefa, excluindo o usuário logado
    tarefas_com_participantes = []
    for tarefa in tarefas_em_grupo:
        participantes = tarefa.participantes.exclude(usuario=usuario).exclude(usuario=tarefa.usuario)
        tarefa_info = {
            'tarefa': tarefa,
            'envolvidos': [tarefa.usuario] if tarefa.usuario != usuario else [],
            'participantes': participantes
        }
        tarefas_com_participantes.append(tarefa_info)

    return render(request, 'menu/tarefas_em_grupo.html', {'tarefas': tarefas_com_participantes})

@login_required
def chat_view(request, user_id):
    recipient = User.objects.get(id=user_id)
    messages = Message.objects.filter(
        (models.Q(sender=request.user) & models.Q(recipient=recipient)) |
        (models.Q(sender=recipient) & models.Q(recipient=request.user))
    ).order_by('timestamp')
    return render(request, 'chat/chat.html', {'messages': messages, 'recipient': recipient})

@login_required
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        recipient_id = data.get('recipient_id')
        content = data.get('content')

        # Verifique se os dados são válidos
        if not recipient_id or not content:
            return JsonResponse({'status': 'Dados inválidos'}, status=400)

        try:
            # Exemplo básico de envio de mensagem
            recipient = User.objects.get(id=recipient_id)
            # Suponha que exista um modelo Message
            Message.objects.create(sender=request.user, recipient=recipient, content=content)
            return JsonResponse({'status': 'Message sent!'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'Usuário não encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'status': f'Erro: {str(e)}'}, status=500)

    return JsonResponse({'status': 'Método inválido'}, status=405)




    