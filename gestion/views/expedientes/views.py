from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, ListView, TemplateView, DetailView, UpdateView, View
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse, reverse_lazy
from gestion.models import EstadoExpediente, Expediente, Registro, Archivo, Cliente, RespuestaCliente
from gestion.forms import ExpedienteForm, RespuestaClienteForm

# ======LISTAR LOS EXPEDIENTES, pasar para otra carpeta llamada expediente con su views.py renombrar el RegistroCreateView por el ListView =======#

class ExpedientesListar(LoginRequiredMixin, ListView):
    model = Expediente
    template_name = 'expedientes/registros_detalles.html'
    context_object_name = 'expedientes'
    permission_required = 'gestion.view_expediente'

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
                expedientes = Expediente.objects.filter(
                    registro_id=registro_id)
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
        context['create_url'] = reverse_lazy(
            'gestion:expediente_crear', kwargs={'pk': registro_id})
        context['home'] = reverse_lazy('gestion:dashboard')
        context['name'] = 'Panel de Control'
        context['entity'] = 'Registros'
        context['registro_id'] = registro_id
        return context


class ExpedienteCreateView(LoginRequiredMixin, CreateView):
    model = Expediente
    form_class = ExpedienteForm
    template_name = 'expedientes/crear.html'
    permission_required = 'gestion.add_expediente'

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
                # Añade campos necesarios
                defaults={'descripcion': 'Estado inicial por defecto'}
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
                    estado_pendiente = EstadoExpediente.objects.get(
                        estado='Pendiente')
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
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        registro_id = self.kwargs['pk']
        registro = Registro.objects.get(pk=registro_id)
        context['title'] = 'Crear Nuevo Expediente'
        context['entity'] = f"Expedientes: {registro.title}"
        context['list_url'] = self.get_success_url()
        context['action'] = 'add'
        context['registro_id'] = self.kwargs['pk']
        context['home'] = reverse_lazy('gestion:dashboard')
        context['name'] = 'Panel de Control'
        return context

class ExpedienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Expediente
    form_class = ExpedienteForm
    template_name = 'expedientes/edit.html'
    success_url = reverse_lazy('gestion:registro_detalle')
    permission_required = 'gestion.change_expediente'

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.registro = get_object_or_404(Registro, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        # Obtiene el expediente usando 'ek' de la URL
        return get_object_or_404(Expediente, pk=self.kwargs['ek'])

    def get_success_url(self):
        return reverse_lazy('gestion:registro_detalle', kwargs={'pk': self.kwargs['pk']})

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                if form.is_valid():
                    expediente = form.save(commit=False)
                    expediente.user = self.request.user
                    expediente.save()
                    form.save_m2m()  # Para relaciones ManyToMany (clientes)
                    for f in request.FILES.getlist('archivos'):
                        Archivo.objects.create(
                            expediente=expediente,
                            archivo=f,
                            nombre=f.name
                        )
                    data = expediente.toJSON()
                else:
                    data['error'] = form.errors.as_json()   
                return JsonResponse(data, safe=False)
            elif action in ['add_resp', 'edit_resp']:
                # Llama a la función que maneja respuestas y retorna directamente
                return self.handle_respuesta_request(request)
            else:
                data['error'] = 'Acción no válida'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get(self, request, *args, **kwargs):
        # AJAX para obtener datos de una respuesta
        respuesta_id = request.GET.get('respuesta_id')
        if respuesta_id:
            try:
                respuesta = RespuestaCliente.objects.get(id=respuesta_id)
                data = {
                    'success': True,
                    'data': {
                        'id': respuesta.id,
                        'expediente_id': respuesta.expediente.id_expediente,
                        'cliente_id': respuesta.cliente.id_cliente,
                        'respuesta': respuesta.respuesta,
                        'evaluacion_gestion': respuesta.evaluacion_gestion,
                        'resultado_gestion': respuesta.resultado_gestion,
                        'fecha_respuesta': respuesta.fecha_respuesta.strftime('%Y-%m-%d') if respuesta.fecha_respuesta else '',
                    }
                }
            except Exception as e:
                data = {'success': False, 'error': str(e)}
            return JsonResponse(data)
        # ...si no es AJAX, sigue el flujo normal...
        return super().get(request, *args, **kwargs)
    
    def handle_respuesta_request(self, request):
        data = {}
        try:
            action = request.POST['action']
                        
            if action == 'add_resp':
                expediente = self.get_object()
                cliente = Cliente.objects.get(pk=request.POST['cliente'])
                #Validacion de Unicidad
                if RespuestaCliente.objects.filter(expediente=expediente, cliente=cliente).exists():
                    data['error'] = 'Ya existe una respuesta para este cliente en este expediente.'
                    return JsonResponse(data)                
                respuesta = RespuestaCliente(
                    expediente=expediente,
                    cliente=cliente,
                    respuesta=request.POST['respuesta'],
                    evaluacion_gestion=request.POST['evaluacion_gestion'],
                    resultado_gestion=request.POST['resultado_gestion'],
                )
                respuesta.save()
                data['success'] = True
                data['message'] = 'Respuesta creada correctamente'
            elif action == 'edit_resp':
                respuesta_id = request.POST.get('id')
                if not respuesta_id:
                    raise ValueError("ID de respuesta no proporcionado")
                respuesta = RespuestaCliente.objects.get(id=respuesta_id)
                respuesta.respuesta = request.POST['respuesta']
                respuesta.evaluacion_gestion = request.POST['evaluacion_gestion']
                respuesta.resultado_gestion = request.POST['resultado_gestion']
                respuesta.fecha_respuesta = request.POST.get('fecha_respuesta')
                respuesta.save()
                data['success'] = True
                data['message'] = 'Respuesta actualizada correctamente'
                
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expediente = self.get_object()
        context['expediente'] = expediente
        registro_id = self.kwargs['pk']
        registro = Registro.objects.get(pk=registro_id)
        context['registro_id'] = self.kwargs['pk']
        context['title'] = 'Investigar Expediente'
        context['entity'] = f"Expedientes: {registro.title}"
        context['expediente_id'] = self.kwargs['ek']
        context['list_url'] = self.get_success_url()
        context['home'] = reverse_lazy('gestion:dashboard')
        context['name'] = 'Panel de Control'
        context['formresp'] = RespuestaClienteForm()
        
        # Diccionario: cliente_id -> respuesta (o None)
        respuestas_por_cliente = {}
        for cliente in expediente.clientes.all():
            respuesta = RespuestaCliente.objects.filter(expediente=expediente, cliente=cliente).first()
            respuestas_por_cliente[cliente.id_cliente] = respuesta
        context['respuestas_por_cliente'] = respuestas_por_cliente
                
        id_cliente = self.request.GET.get('id_cliente') or self.request.POST.get('cliente')  # O como lo recibas
        if id_cliente:
            cliente = get_object_or_404(Cliente, id_cliente=id_cliente, expediente=expediente).first()
            # Si el cliente existe, inicializa el formulario con ese cliente
            formresp = RespuestaClienteForm(initial={'cliente': cliente}, expediente=expediente)
            formresp.fields['cliente'].queryset = Cliente.objects.filter(id_cliente=id_cliente)
            
            context['cliente'] = cliente
            context['formresp'] = formresp
        
            # Obtener respuestas existentes (opcional)
            context['respuestas'] = RespuestaCliente.objects.filter(
                expediente=expediente, cliente=cliente)
            
            # Obtener todos los clientes del expediente
            context['clientes'] = expediente.clientes.all()
                 
        return context

