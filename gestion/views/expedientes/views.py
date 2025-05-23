from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, ListView, TemplateView, DetailView, UpdateView
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from gestion.models import EstadoExpediente, Expediente, Registro, Archivo
from gestion.forms import ExpedienteForm

#======LISTAR LOS EXPEDIENTES, pasar para otra carpeta llamada expediente con su views.py renombrar el RegistroCreateView por el ListView =======#

class ExpedientesListar(LoginRequiredMixin, ListView):
    model = Expediente
    template_name = 'expedientes/registros_detalles.html'
    context_object_name = 'expedientes'
    permission_required = 'view_expediente'
    
    def get_queryset(self):
        # Obtener el registro específico basado en el ID pasado en la URL
        registro_id = self.kwargs['pk']
        return Expediente.objects.filter(registro_id=registro_id).order_by('-fecha_create')
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                registro_id = self.kwargs['pk']
                expedientes = Expediente.objects.filter(registro_id=registro_id)
                data = [expediente.toJSON() for expediente in expedientes]
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        registro_id = self.kwargs['pk']
        registro = Registro.objects.get(pk=registro_id)
        # Mostrar el título del registro
        context['title'] = f"Detalles del Registro: {registro.title}"        
        context['list_url'] = reverse_lazy('gestion:registros')
        context['create_url'] = reverse_lazy('gestion:expediente_crear', kwargs={'pk': registro_id})
        context['home'] = reverse_lazy('gestion:dashboard')
        context['name'] = 'Panel de Control'
        context['entity'] = 'Registros'
        context['registro_id'] = registro_id 
        return context
    
class ExpedienteCreateView(LoginRequiredMixin, CreateView):
    model = Expediente
    form_class = ExpedienteForm
    template_name = 'expedientes/crear.html'
    permission_required = 'add_expediente'
    
    @method_decorator(csrf_exempt)        
    def dispatch(self, request, *args, **kwargs):
        self.registro = get_object_or_404(Registro, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Solo los campos básicos para la creación
        kwargs['fields'] = [
            'title', 'procedencia', 'fecha_entrega', 'clientes', 'clasificacion', 'ueb_obets', 'reclamacion'
        ]
        return kwargs
    
    def form_valid(self, form):
        try:
            # 1. Obtener o crear el estado "Pendiente" si no existe
            estado_pendiente, created = EstadoExpediente.objects.get_or_create(
                estado='Pendiente',
                defaults={'descripcion': 'Estado inicial por defecto'}  # Añade campos necesarios
            )
        except Exception as e:
            # Manejar errores inesperados
            form.add_error(None, f"Error al asignar el estado: {str(e)}")
            return self.form_invalid(form)
        
        # 2. Asignar valores al expediente
        expediente = form.save(commit=False)
        expediente.estado_expediente = estado_pendiente
        expediente.registro = self.registro
        expediente.user = self.request.user
        
        # 3. Guardar una sola vez y evitar super().form_valid()
        expediente.save()
        form.save_m2m()  # Necesario para relaciones ManyToMany (clientes)
        # 4. Redirigir manualmente sin guardar de nuevo
        return HttpResponseRedirect(self.get_success_url())
    
        
    def get_success_url(self):
        return reverse_lazy('gestion:registro_detalle', kwargs={'pk': self.kwargs['pk']})
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                if form.is_valid():
                    expediente = form.save(commit=False)
                    estado_pendiente = EstadoExpediente.objects.get(estado='Pendiente')
                    expediente.estado_expediente = estado_pendiente
                    expediente.registro = self.registro
                    expediente.user = self.request.user
                    expediente.save()
                    form.save_m2m()
                    
                    data = expediente.toJSON()
                else:
                    data['error'] = form.errors.as_json()
            else:
                data['error'] = 'Acción no válida'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe = False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Nuevo Expediente'
        context['entity'] = 'Expediente'
        context['list_url'] = self.get_success_url()
        context['action'] = 'add'
        context['registro_id'] = self.kwargs['pk']
        context['home'] = reverse_lazy('gestion:dashboard')
        context['name'] = 'Panel de Control'
        return context
    
class ExpedienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Expediente
    form_class = ExpedienteForm
    # template_name = 
    # permission_required = 
    
    # Procesar archivos subidos
    # archivos = self.request.FILES.getlist('archivos')
    # for archivo in archivos:
    #     Archivo.objects.create(
    #         expediente=self.object,
    #         archivo=archivo,
    #         nombre=archivo.name
    #     )
    # return super().form_valid(form)