# # Vista para manejar acciones de respuesta
# from django.http import JsonResponse
# from django.views import View

# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator

# from django.contrib.auth.mixins import LoginRequiredMixin
# from gestion.forms import RespuestaClienteForm
# from gestion.mixin import ValidatePermissionRequiredMixin

# from gestion.models import Cliente, Expediente, RespuestaCliente

# # class RespuestaSaveView(LoginRequiredMixin, ValidatePermissionRequiredMixin, View):
# #     permission_required = ('gestion.add_respuestacliente', 'gestion.view_respuestacliente', 'gestion.change_respuestacliente')
# #     model = RespuestaCliente
    
# #     @method_decorator(csrf_exempt)
# #     def dispatch(self, request, *args, **kwargs):
# #         return super().dispatch(request, *args, **kwargs)
        
# #     def get(self, request, *args, **kwargs):
# #         data = {}
# #         try:
# #             respuesta_id = request.GET.get('respuesta_id')
# #             expediente_id = request.GET.get('expediente_id')
# #             cliente_id = request.GET.get('cliente_id')
            
# #             if respuesta_id:
# #                 # Editar respuesta existente
# #                 respuesta = RespuestaCliente.objects.filter(id=respuesta_id)
# #             else:
# #                 # Crear nueva respuesta
# #                 respuesta = RespuestaCliente()
# #                 respuesta.expediente_id = expediente_id
# #                 respuesta.cliente_id = cliente_id   
# #                 respuesta.user = request.user
# #             #Actualizar campos
# #             respuesta.respuesta = request.POST.get('respuesta')
# #             respuesta.evaluacion_gestion = request.POST.get('evaluacion_gestion')
# #             respuesta.resultado_gestion = request.POST.get('resultado_gestion')
# #             respuesta.fecha_respuesta = request.POST.get('fecha_respuesta')
# #             respuesta.save()
            
# #             data['success'] = True
# #         except Exception as e:
# #             data['error'] = str(e)
# #         return JsonResponse(data)
    
# #     def get_context_data(self, **kwargs):
# #         context = super().get_context_data(**kwargs)
# #         return context
    
    
# # class RespuestaGetView(LoginRequiredMixin, View):
# #     def get(self, request, respuesta_id, *args, **kwargs):
# #         data = {'success': False}
# #         try:
# #             respuesta = RespuestaCliente.objects.get(id=respuesta_id)
# #             cliente = respuesta.cliente
            
# #             data = {
# #                 'success': True,
# #                 'data': {
# #                     'id': respuesta.id,
# #                     'expediente_id': respuesta.expediente_id,
# #                     'cliente_id': respuesta.cliente_id,
# #                     'cliente_nombre': f"{cliente.nombre} {cliente.apellido}",
# #                     'respuesta': respuesta.respuesta,
# #                     'evaluacion_gestion': respuesta.evaluacion_gestion,
# #                     'resultado_gestion': respuesta.resultado_gestion,
# #                     'fecha_respuesta': respuesta.fecha_respuesta.strftime('%Y-%m-%d'),
# #                 }
# #             }
# #         except Exception as e:
# #             data['error'] = str(e)
# #         return JsonResponse(data)

# # class RespuestaPrintView(LoginRequiredMixin, View):
# #     def get(self, request, respuesta_id, *args, **kwargs):
# #         # Implementar lógica para generar PDF
# #         # return HttpResponse("PDF generado")
# #         pass

# class RespuestaSaveView(LoginRequiredMixin,View):
#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         data = {}
#         try:
#             action = request.POST['action']
#             if action == 'add_resp':
#                 expediente_id = request.POST['expediente_id']
#                 id_cliente = request.POST['id_cliente']
#                 expediente = Expediente.objects.get(pk=expediente_id)
#                 cliente = Cliente.objects.get(pk=id_cliente)
#                 evaluacion_gestion=request.POST['evaluacion_gestion']
#                 resultado_gestion=request.POST['resultado_gestion']
#                 form = RespuestaClienteForm(request.POST)
#                 if form.is_valid():
#                     respuesta = form.save(commit=False)
#                     respuesta.expediente = expediente
#                     respuesta.cliente = cliente
#                     respuesta.save()
#                     data['success'] = True
#                     data['message'] = 'Respuesta creada correctamente'
#                 else:
#                     data['error'] = form.errors.as_json()
#             elif action == 'edit_resp':
#                 respuesta = RespuestaCliente.objects.get(id=request.POST['id'])
#                 form = RespuestaClienteForm(request.POST, instance=respuesta)
#                 if form.is_valid():
#                     form.save()
#                     data['success'] = True
#                     data['message'] = 'Respuesta actualizada correctamente'
#                 else:
#                     data['error'] = form.errors.as_json()
#             else:
#                 data['error'] = 'Acción no válida'
#         except Exception as e:
#             data['error'] = str(e)
#         return JsonResponse(data)


# # Vista para obtener datos de respuesta
# class RespuestaGetView(View):
#     def get(self, request, *args, **kwargs):
#         data = {'success': False}
#         try:
#             respuesta = RespuestaCliente.objects.get(id=id)
#             cliente = respuesta.cliente
#             data = {
#                 'success': True,
#                 'data': {
#                     'id': respuesta.id,
#                     'expediente_id': respuesta.expediente_id,
#                     'id_cliente': respuesta.id_cliente,
#                     'cliente_nombre': f"{cliente.nombre} {cliente.apellido}",
#                     'respuesta': respuesta.respuesta,
#                     'evaluacion_gestion': respuesta.evaluacion_gestion,
#                     'resultado_gestion': respuesta.resultado_gestion,
#                     'fecha_respuesta': respuesta.fecha_respuesta.strftime('%Y-%m-%d'),
#                 }
#             }
#         except Exception as e:
#             data['error'] = str(e)
#         return JsonResponse(data)
        