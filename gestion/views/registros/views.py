from django.views.generic import CreateView, ListView, TemplateView, DetailView
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from gestion.models import Registro
from gestion.forms import RegistroForm

#======VISTA DE REGISTROS=======#
class RegistroListarView(LoginRequiredMixin, TemplateView):
    model = Registro
    template_name = 'registros/registros.html'
    
    @method_decorator(csrf_exempt)
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
        context['home'] = reverse_lazy('gestion:dashboard')
        context['name'] = 'Panel de Control'
        context['form'] = RegistroForm()
        return context

    def get_queryset(self):
        return Registro.objects.all().order_by('-fecha_creacion')
  

  
