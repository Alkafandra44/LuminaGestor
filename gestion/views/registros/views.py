from django.views.generic import CreateView, ListView
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from gestion.models import Registro
from gestion.forms import RegistroForm

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

class RegistroListarView(ListView):
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
                    data.append({
                        'id_registro': i.id_registro,
                        'title': i.title,
                        'fecha_creacion': i.fecha_creacion,
                    })
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
        return context

    def get_queryset(self):
        return Registro.objects.all().order_by('-fecha_creacion')