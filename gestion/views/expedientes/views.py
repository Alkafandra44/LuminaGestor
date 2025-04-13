from django.views.generic import CreateView, ListView, TemplateView, DetailView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from gestion.models import Expediente
from gestion.forms import ExpedienteForm

#======LISTAR LOS EXPEDIENTES, pasar para otra carpeta llamada expediente con su views.py renombrar el RegistroCreateView por el ListView =======#

class ExpedienteListView(ListView):
    model = Expediente
    template_name = 'registro/registros_detalles.html'
    context_object_name = 'expediente'
    
    
    