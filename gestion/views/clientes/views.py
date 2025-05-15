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
    permission_required = ('gestion.add_cliente')
    model = Cliente
    template_name = 'clientes/clientes.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                clientes = Cliente.objects.all()
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
                cliente = Cliente()
                cliente.carnet = request.POST['carnet']
                cliente.nombre = request.POST['nombre']
                cliente.apellido = request.POST['apellido']
                cliente.telefono = request.POST['telefono']
                cliente.direccion = request.POST['direccion']
                cliente.municipio_id = request.POST['municipio']
                cliente.save()
            elif action == 'edit':
                cliente = Cliente.objects.get(pk=request.POST['id'])
                cliente.carnet = request.POST['carnet']
                cliente.nombre = request.POST['nombre']
                cliente.apellido = request.POST['apellido']
                cliente.telefono = request.POST['telefono']
                cliente.direccion = request.POST['direccion']
                cliente.municipio_id = request.POST['municipio']
                cliente.save()
            elif action == 'delete':
                cliente = Cliente.objects.get(pk=request.POST['id'])
                cliente.delete()
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
        context['name'] = 'Home'
        context['entity'] = 'Clientes'
        context['form'] = ClienteForm()
        return context

class ClienteCreateViews(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/crear.html'
    
    # @method_decorator(login_required)
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form() #De esta forma tambien se obtienen los datos del formulario
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    
    
    #     print(request.POST)
    #     form = ClienteForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return HttpResponseRedirect(self.success_url)
    #     self.object = None
    #     context = self.get_context_data(**kwargs)
    #     context['form'] = form
    #     return render(request,self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Cliente'
        context['list_url'] = reverse_lazy('gestion:clientes')
        context['entity'] = 'Clientes'
        context['action'] = 'add'
        
        return context

class ClienteUpdateViews(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/crear.html'
    success_url = reverse_lazy('gestion:clientes')
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form() #De esta forma tambien se obtienen los datos del formulario
                data = form.save()
            else:
                data['error'] = 'Error al editar'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    
    def get_context_data(self, **kwargs):
        print(self.object)
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Cliente'
        context['list_url'] = reverse_lazy('gestion:clientes')
        context['entity'] = 'Clientes'
        context['action'] = 'edit'
        return context
    
class ClienteDeleteViews(DeleteView):
    model = Cliente
    template_name = 'clientes/delete.html'
    success_url = reverse_lazy('gestion:clientes')
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
            return JsonResponse(data)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Cliente'
        context['list_url'] = reverse_lazy('gestion:clientes')
        context['entity'] = 'Clientes'
        return context
    
