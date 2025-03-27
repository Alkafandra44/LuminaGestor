#from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import FormView, RedirectView
from django.shortcuts import redirect, HttpResponseRedirect
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
import SystemDjango.settings as setting

# Create your views here.   
class LoginFormView1(FormView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = reverse_lazy('gestion:clientes')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(setting.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.success_url)
    
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        context['title'] = 'Inicio de Sesión'
        return context
    
class LogoutRedirectView(RedirectView):
    pattern_name = 'login'
    
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)
    