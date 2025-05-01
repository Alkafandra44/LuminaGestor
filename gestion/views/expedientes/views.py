from django.views.generic import CreateView, ListView, TemplateView, DetailView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from gestion.models import Expediente, Registro
from gestion.forms import ExpedienteForm1

#======LISTAR LOS EXPEDIENTES, pasar para otra carpeta llamada expediente con su views.py renombrar el RegistroCreateView por el ListView =======#

class ExpedientesListar(LoginRequiredMixin, ListView):
    model = Expediente
    template_name = 'expedientes/registros_detalles.html'
    context_object_name = 'expedientes'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                expediente = Expediente.objects.all()
                data = []
                for i in Expediente.objects.all():
                    data.append(i.toJSON())
            #     for i in expediente:
            #         data.append({
            #             'id_expediente': i.id_expediente,
            #             'title': i.title,
            #             'fecha_complete': i.fecha_complete,
            #             'clientes': i.clientes,
            #             'clasificacion': i.clasificacion,
            #             'procedencia': i.procedencia,
            #             'ueb_obets': i.ueb_obets,
            #             'estado_expediente': i.estado_expediente,
            #         })
            # elif action == 'add':
            #     expediente = Expediente()
            #     expediente.title = request.POST['title']
            #     expediente.fecha_complete = request.POST['fecha_complete']
                
            #     #=====CAMBIAR LA LOGICA DE EXPEDIENTE PARA ELEGIR MULTIPLES CLIENTES=====
            #     #expediente.clientes = request.POST['clientes']
                
            #     expediente.clasificacion = request.POST['clasificacion']
            #     expediente.procedencia = request.POST['procedencia']
            #     expediente.ueb_obets = request.POST['ueb_obets']
            #     expediente.save()
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
        context['home'] = reverse_lazy('gestion:dashboard')
        context['name'] = 'Home'
        context['entity'] = 'Expediente'
        return context
    
class ExpedienteCreateView(LoginRequiredMixin, CreateView):
    model = Expediente
    form_class = ExpedienteForm1
    template_name = 'expedientes/crear.html'
    
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Expediente'
        context['entity'] = 'Expediente'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['home'] = reverse_lazy('gestion:dashboard')
        context['name'] = 'Home'
        context['entity'] = 'Expediente'
        return context
    