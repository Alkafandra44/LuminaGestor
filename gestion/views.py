from django.shortcuts import render, redirect
#PARA VISTAS BASADAS EN CLASES
from django.views.generic import ListView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import ExpedienteForm
from .models import *


# Create your views here.
def home(request):
    data ={
        'title': 'Bienvenido'
    }
    return render(request, 'home.html', data)


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
    data = {
        'title': 'Listado de Clientes',
        'clientes': Cliente.objects.all()
    }
    return render(request, 'clientes/clientes.html', data)

##=====EJEMPLO DE VISTA BASADAS EN CLASES====####
class ClienteListar(ListView):
    model = Cliente
    template_name = 'clientes/clientes.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Clientes'
        
        return context



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
        
