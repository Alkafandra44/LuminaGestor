from django.http import JsonResponse
from django.views import View
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin

from gestion.models import Archivo

@method_decorator(csrf_exempt, name='dispatch')
class ArchivoDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            archivo_id = request.POST.get('archivo_id')
            archivo = Archivo.objects.get(id=archivo_id)
            archivo.archivo.delete()  # Borra el archivo físico
            archivo.delete()
            data['success'] = True
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)