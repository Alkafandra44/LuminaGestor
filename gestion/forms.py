from django.forms import ModelForm
from .models import Expediente, Cliente

class ExpedienteForm(ModelForm):
    class Meta:
        model = Expediente
        fields = ['title', 'resumen','importan']
        
#class Registro()

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        