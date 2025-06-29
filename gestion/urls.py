from django.urls import path
#from gestion.views import *
from gestion.views.archivos.view import *
from gestion.views.dashboard.views import *
from gestion.views.clientes.views import *
from gestion.views.modelos.views import *
from gestion.views.registros.views import *
from gestion.views.expedientes.views import *
from gestion.views.respuestas.view import *


app_name = 'gestion'

urlpatterns = [
    
    #registros
    path('registros/', RegistroListarView.as_view(), name="registros"),
    path('registros/detalle/<int:pk>/', ExpedientesListar.as_view(), name="registro_detalle"), 
    
    #expedientes
    path('registros/detalle/<int:pk>/expediente/add/', ExpedienteCreateView.as_view(), name="expediente_crear"),
    path('registros/detalle/<int:pk>/expediente/show/<int:ek>/', ExpedienteTempalteView.as_view(), name="expediente_show"),
    path('registros/detalle/<int:pk>/expediente/update/<int:ek>/', ExpedienteUpdateView.as_view(), name="expediente_editar"),
    path('expedientes/resumen/pdf/', ResumenPDFView.as_view(), name='expediente_resumen_pdf'),
    
    
    #respuestas
    path('respuesta/pdf/<int:respuesta_id>/', ExpedienteInvoivePdfView.as_view(), name="respuesta_pdf"),
   
    path('archivo/delete/', ArchivoDeleteView.as_view(), name='archivo_delete'),
    
    #clientes
    path('clientes/', ClienteListar.as_view(), name="clientes"),

    #Home
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    
    
]
