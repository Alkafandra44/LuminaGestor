from django.views.generic import TemplateView
from django.urls import reverse_lazy

class DashboardView(TemplateView):
    template_name = 'dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Panel de administrador'
        context['home'] = reverse_lazy('gestion:dashboard')
        context['name'] = 'Panel de administrador'
        return context
    
   