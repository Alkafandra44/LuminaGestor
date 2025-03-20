from django.urls import path
from gestion.views import *

app_name = 'gestion'

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name="signup"),
    path('gestion/', gestion, name="gestion"),
    path('expediente/create/', create_expediente, name="create_expediente"),
    path('usuarios/', usuarios, name="usuarios"),
    path('clientes/', ClienteListar.as_view(), name="clientes"),
    path('clientes/add', ClienteCreateViews.as_view(), name="clientes_crear"),
    path('logout/', signout, name="logout"),
    path('signin/', signin, name="signin")
]
