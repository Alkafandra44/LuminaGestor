from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView

from user.models import User
from user.forms import UserForm

# Create your views here.
class UsersListView(ListView):
    model = User
    template_name = 'user/user.html'
    #====permission_required = 'user.view_user'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in User.objects.all():
                    data.append(i.toJSON())
            elif action == 'add':
                form = UserForm(request.POST, request.FILES)
                form.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Usuarios'
        context['list_url'] = reverse_lazy('user:user_list')
        context['entity'] = 'Usuarios'
        context['home'] = reverse_lazy('gestion:dashboard')
        context['name'] = 'Home'
        context['form'] = UserForm()
        return context
    
class UserCreateView(CreateView): #LoginRequiredMixin, ValidatePermissionRequiredMixin ()
    model = User
    form_class = UserForm
    template_name = 'user/user.html'
    success_url = reverse_lazy('user:user_list')
    # permission_required = 'user.add_user'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                # data = form.save()
                
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de un Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context