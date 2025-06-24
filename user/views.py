from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.generic import ListView

from user.models import User
from user.forms import UserForm

# Create your views here.
class UsersListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'user/user.html'
    #permission_required = 'user.view_user'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                usuario = User.objects.all()
                data = []
                for usuario in usuario:
                    user_data = {
                        'id': usuario.id,
                        'first_name': usuario.first_name,
                        'last_name': usuario.last_name,
                        'username': usuario.username,
                        'email': usuario.email,
                        'groups': [group.name for group in usuario.groups.all()],
                        'groups_id': [group.id for group in usuario.groups.all()],
                        'date_joined': usuario.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
                        'is_superuser': usuario.is_superuser,  
                    }
                    data.append(user_data)
            elif action == 'add':
                if not request.user.has_perm('user.add_user'):
                    return JsonResponse({'error': 'No tienes permiso para agregar usuarios.'}, status=403)
                usuario = User()
                usuario.first_name = request.POST['first_name']
                usuario.last_name = request.POST['last_name']
                usuario.username = request.POST['username']
                usuario.email = request.POST['email']
                usuario.set_password (request.POST['password'])
                usuario.save()
                grupos = request.POST.getlist('groups')
                if grupos:
                    usuario.groups.set(grupos)
            elif action == 'edit':
                if not request.user.has_perm('user.change_user'):
                    return JsonResponse({'error': 'No tienes permiso para editar usuarios.'}, status=403)
                usuario = User.objects.get(pk=request.POST['id'])
                usuario.first_name = request.POST['first_name']
                usuario.last_name = request.POST['last_name']
                usuario.username = request.POST['username']
                usuario.email = request.POST['email']
                usuario.groups.set(request.POST.getlist('groups'))
                
                # Encriptar la contraseña solo si se proporciona una nueva
                if 'password' in request.POST and request.POST['password']:
                    usuario.set_password(request.POST['password'])  # Encripta la nueva contraseña
                
                usuario.save()
            elif action == 'delete':
                if not request.user.has_perm('user.delete_user'):
                    return JsonResponse({'error': 'No tienes permiso para eliminar usuarios.'}, status=403)
                usuario = User.objects.get(pk=request.POST['id'])
                usuario.delete()
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
        context['name'] = 'Panel de Control'
        context['form'] = UserForm()
        return context
    