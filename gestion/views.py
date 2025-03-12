from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import ExpedienteForm


# Create your views here.
def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # Registrar Usuario
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('gestion')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'El usuario ya existe'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            "error": 'La contraseña no coincide'
        })


def gestion(request):
    return render(request, 'gestion.html')

def create_expediente(request):
    if request.method == 'GET':
        return render(request, 'create_expediente.html', {
            'form': ExpedienteForm
        })
    else:
        try:
            form = ExpedienteForm(request.POST)
            new_exp = form.save(commit=False)
            new_exp.user = request.user
            new_exp.save()
            return redirect(gestion)
        except:
            return render(request, 'create_expediente.html', {
            'form': ExpedienteForm,
            'error': 'Agregue un dato valido'
        })


def usuarios(request):
    return render(request, 'usuarios.html')


def clientes(request):
    return render(request, 'clientes.html')


def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrecto'
            })
        else:
            login(request, user)
            return redirect('gestion')
        
