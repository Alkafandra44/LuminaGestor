# views.py
from django.http import JsonResponse

from gestion.models import RespuestaCliente

def get_respuesta(request, respuesta_id):
    try:
        respuesta = RespuestaCliente.objects.get(id=respuesta_id)
        data = {
            'success': True,
            'data': {
                'id': respuesta.id,
                'expediente_id': respuesta.expediente.id,
                'cliente_id': respuesta.cliente.id_cliente,
                'respuesta': respuesta.respuesta,
                'evaluacion_gestion': respuesta.evaluacion_gestion,
                'resultado_gestion': respuesta.resultado_gestion,
                'fecha_respuesta': respuesta.fecha_respuesta.strftime('%Y-%m-%d'),
            }
        }
        return JsonResponse(data)
    except RespuestaCliente.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Respuesta no encontrada'}, status=404)