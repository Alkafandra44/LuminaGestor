from gestion.models import Expediente

def notificaciones_expedientes(request):
    user = request.user
    return {
        'exp_investigacion': Expediente.objects.filter(estado_expediente__estado='Investigación').count(),
        'exp_corregir': Expediente.objects.filter(estado_expediente__estado='Corregir').count(),
        'is_director': user.groups.filter(name='Director').exists(),
        'is_tecnico': user.groups.filter(name='Técnicos').exists(),
        'is_admin': user.is_superuser or user.is_staff,
    }