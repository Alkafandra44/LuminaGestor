from django.shortcuts import render, redirect
from django.http import JsonResponse

# PARA VISTAS BASADAS EN CLASES
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required

from gestion.forms import ClienteForm
from gestion.mixin import ValidatePermissionRequiredMixin
from gestion.models import *

# Create your views here.


## ===== USO DE VISTA BASADAS EN CLASES====##

class ClienteListar(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Cliente
    template_name = 'clientes/clientes.html'
    permission_required = 'gestion.view_cliente'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                clientes = Cliente.objects.filter(is_delete=False)
                data = []
                for i in clientes:
                    data.append({
                        'id_cliente': i.id_cliente,
                        'carnet': i.carnet,
                        'nombre': i.nombre,
                        'apellido': i.apellido,
                        'direccion': i.direccion,
                        'telefono': i.telefono,
                        'municipio': i.municipio.nombre if i.municipio else None,
                        'municipio_id': i.municipio.id_municipio if i.municipio else None,  # Añade esto
                    })
            elif action == 'add':
                if not request.user.has_perm('gestion.add_cliente'):
                    return JsonResponse({'error': 'No tienes permiso para agregar clientes.'}, status=403)
                cliente = Cliente()
                cliente.carnet = request.POST['carnet']
                cliente.nombre = request.POST['nombre']
                cliente.apellido = request.POST['apellido']
                cliente.telefono = request.POST['telefono']
                cliente.direccion = request.POST['direccion']
                cliente.municipio_id = request.POST['municipio']
                cliente.save()
            elif action == 'edit':
                if not request.user.has_perm('gestion.change_cliente'):
                    return JsonResponse({'error': 'No tienes permiso para editar clientes.'}, status=403)
                cliente = Cliente.objects.get(pk=request.POST['id'])
                cliente.carnet = request.POST['carnet']
                cliente.nombre = request.POST['nombre']
                cliente.apellido = request.POST['apellido']
                cliente.telefono = request.POST['telefono']
                cliente.direccion = request.POST['direccion']
                cliente.municipio_id = request.POST['municipio']
                cliente.save()
            elif action == 'delete':
                if not request.user.has_perm('gestion.delete_cliente'):
                    return JsonResponse({'error': 'No tienes permiso para eliminar clientes.'}, status=403)
                cliente = Cliente.objects.get(pk=request.POST['id'])
                cliente.is_delete = True
                cliente.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Clientes'
        context['create_url'] = reverse_lazy('gestion:clientes_crear')
        context['list_url'] = reverse_lazy('gestion:clientes')
        context['home'] = reverse_lazy('gestion:dashboard')
        context['name'] = 'Panel de Control'
        context['entity'] = 'Clientes'
        context['form'] = ClienteForm()
        return context
