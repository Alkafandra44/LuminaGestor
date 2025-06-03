# Vista para manejar acciones de respuesta
from django.http import JsonResponse
from django.views import View

from gestion.models import RespuestaCliente


class RespuestaAccionView(View):
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            expediente_id = request.POST['expediente_id']
            cliente_id = request.POST['cliente_id']
            
            if action == 'add':
                respuesta = RespuestaCliente(
                    expediente_id=expediente_id,
                    cliente_id=cliente_id,
                    respuesta=request.POST['respuesta'],
                    evaluacion_gestion=request.POST['evaluacion_gestion'],
                    resultado_gestion=request.POST['resultado_gestion'],
                    user=request.user
                )
                respuesta.save()
                data['success'] = True
                data['message'] = 'Respuesta creada correctamente'
                
            elif action == 'edit':
                respuesta = RespuestaCliente.objects.get(id=request.POST['id'])
                respuesta.respuesta = request.POST['respuesta']
                respuesta.evaluacion_gestion = request.POST['evaluacion_gestion']
                respuesta.resultado_gestion = request.POST['resultado_gestion']
                respuesta.save()
                data['success'] = True
                data['message'] = 'Respuesta actualizada correctamente'
                
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


# Vista para obtener datos de respuesta
class GetRespuestaView(View):
    def get(self, request, *args, **kwargs):
        try:
            respuesta_id = request.GET.get('id')
            respuesta = RespuestaCliente.objects.get(id=respuesta_id)
            data = {
                'respuesta': {
                    'id': respuesta.id,
                    'expediente_id': respuesta.expediente_id,
                    'cliente_id': respuesta.cliente_id,
                    'respuesta': respuesta.respuesta,
                    'evaluacion_gestion': respuesta.evaluacion_gestion,
                    'resultado_gestion': respuesta.resultado_gestion
                }
            }
            return JsonResponse(data)
        except RespuestaCliente.DoesNotExist:
            return JsonResponse({'error': 'Respuesta no encontrada'}, status=404)
        