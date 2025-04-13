from django.urls import path
#from gestion.views import *
from gestion.views.dashboard.views import *
from gestion.views.clientes.views import *
from gestion.views.registros.views import *


app_name = 'gestion'

urlpatterns = [
    path('signup/', signup, name="signup"),
    path('signin/', signin, name="signin"),
    
    #registros
    path('registros/', RegistroListarView.as_view(), name="registros"),
    path('registros/create/', RegistroCreateView.as_view(), name="registros_crear"), 
    path('registros/detalle/<int:pk>/', ExpedientesListar.as_view(), name="registro_detalle"), 
    
    #expedientes
    #path('expediente/create/', create_expediente, name="create_expediente"),
    
    #usuarios
    path('usuarios/', usuarios, name="usuarios"),
    
    #clientes
    path('clientes/', ClienteListar.as_view(), name="clientes"),
    path('clientes/add', ClienteCreateViews.as_view(), name="clientes_crear"),
    path('clientes/edit/<int:pk>/', ClienteUpdateViews.as_view(), name="clientes_editar"),
    path('clientes/delete/<int:pk>/', ClienteDeleteViews.as_view(), name="clientes_eliminar"),
    
    #Home
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    
    
]
