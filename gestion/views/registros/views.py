from django.views.generic import CreateView, ListView, TemplateView, DetailView
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from gestion.models import Registro, Expediente
from gestion.forms import RegistroForm, ExpedienteForm


#======VISTA DE REGISTROS=======#
class RegistroListarView(TemplateView):
    model = Registro
    template_name = 'registros/registros.html'
    
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                registros = Registro.objects.all()
                data = []
                for i in registros:
                    data.append(i.toJSON())
            elif action == 'add':
                registro = Registro()
                registro.title = request.POST['title']
                registro.save()
            elif action =='edit':
                registro = Registro.objects.get(pk=request.POST['id'])
                registro.title = request.POST['title']
                registro.save()
            elif action =='delete':
                registro = Registro.objects.get(pk=request.POST['id'])
                registro.delete()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro'
        context['list_url'] = reverse_lazy('gestion:registros')
        context['create_url'] = reverse_lazy('gestion:registros_crear')
        context['entity'] = 'Registros'
        context['form'] = RegistroForm()
        return context

    def get_queryset(self):
        return Registro.objects.all().order_by('-fecha_creacion')
  
#======CREAR REGISTRO=======# 
class RegistroCreateView(CreateView):
    model = Registro
    form_class = RegistroForm
    template_name =  'registros/crear.html'
    success_url = reverse_lazy('gestion:registros')  # Cambia esto según tu URL de listado de registros

    def post(self, request, *args, **kwargs):
        data = request.POST
        print(data)
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form() #De esta forma tambien se obtienen los datos del formulario
                print(form)
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Registro'
        context['list_url'] = reverse_lazy('gestion:registros')
        context['entity'] = 'Registros'
        context['action'] = 'add'
        return context
  
#======CONTENIDO DE REGISTRO DETALLE=======#
class ExpedientesListar(ListView):
    model = Expediente
    template_name = 'registros/registros_detalles.html'
    context_object_name = 'expedientes'
    
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                registros = Expediente.objects.filter(registro_id=request.POST['id_expediente'])
                data = []
                for i in registros:
                    data.append(i.toJSON())
            elif action == 'add':
                form = ExpedienteForm(request.POST)
                if form.is_valid():
                    form.save()
                    data['success'] = 'Expediente creado correctamente'
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_queryset(self):
        # Obtener el registro específico basado en el ID pasado en la URL
        registro_id = self.kwargs['pk']
        return Expediente.objects.filter(registro_id=registro_id).order_by('-fecha_create')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        registro_id = self.kwargs['pk']
        registro = Registro.objects.get(pk=registro_id)
        # Mostrar el título del registro
        context['title'] = f"Detalles del Registro: {registro.title}"
        context['list_url'] = reverse_lazy('gestion:registros')
        return context
    