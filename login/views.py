from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import RegisterForm, LoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from .models import Usuario

def login(request):
    if request.method == 'POST':
        print("POST recebido no login")  # Verifica se o POST foi recebido
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('menu')  # Redireciona para o menu após o login
        else:
            print("Erros no formulário:", form.errors)  # Mostra os erros do formulário
    else:
        form = LoginForm()
    return render(request, 'login/login.html', {'form': form})

def save(self, commit=True):
    # Cria o usuário sem salvar no banco ainda
    user = super(RegisterForm, self).save(commit=False)
    user.email = self.cleaned_data['email']
    user.set_password(self.cleaned_data['password1'])  # Define a senha corretamente
    
    # Salva o usuário no banco se commit for True
    if commit:
        user.save()
        # Adiciona os dados do modelo Usuario com os campos adicionais
        usuario = Usuario.objects.create(
            user=user,
            usuario=self.cleaned_data.get('username'),  # Inclui o campo nome no modelo Usuario
            escolaridade=self.cleaned_data.get('escolaridade'),
            data_nascimento=self.cleaned_data.get('data_nascimento'),
            escola=self.cleaned_data.get('escola')
        )
        usuario.save()  # Salva a instância de Usuario no banco

    return user


def register(request):
    if request.method == 'POST':
        print("POST recebido")
        form = RegisterForm(request.POST)
        if form.is_valid():
            print("Formulário válido")
            form.save()
            return redirect('login')
        else:
            print("Erros no formulário:", form.errors)
    else:
        form = RegisterForm()
    return render(request, 'login/register.html', {'form': form})

    
def user_logout(request):
    auth_logout(request)
    return redirect('login')


    from django.views.decorators.csrf import csrf_protect

