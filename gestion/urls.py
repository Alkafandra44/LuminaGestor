from django.urls import path
#from gestion.views import *
from gestion.views.dashboard.views import *
from gestion.views.clientes.views import *
from gestion.views.registros.views import *
from gestion.views.expedientes.views import *


app_name = 'gestion'

urlpatterns = [
    
    #registros
    path('registros/', RegistroListarView.as_view(), name="registros"),
    path('registros/detalle/<int:pk>/', ExpedientesListar.as_view(), name="registro_detalle"), 
    
    #expedientes
    path('registros/detalle/<int:pk>/expediente/add/', ExpedienteCreateView.as_view(), name="expediente_crear"),
    # path('registros/detalle/<int:pk>/expediente/show/<int:ek>', ExpedienteTempalteView.as_view(), name="expediente_show"),
    path('registros/detalle/<int:pk>/expediente/update/<int:ek>/', ExpedienteUpdateView.as_view(), name="expediente_editar"),
    
    #clientes
    path('clientes/', ClienteListar.as_view(), name="clientes"),
    path('clientes/add', ClienteCreateViews.as_view(), name="clientes_crear"),
    path('clientes/edit/<int:pk>/', ClienteUpdateViews.as_view(), name="clientes_editar"),
    path('clientes/delete/<int:pk>/', ClienteDeleteViews.as_view(), name="clientes_eliminar"),
    
    #Home
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    
    
]
