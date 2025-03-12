from django.forms import ModelForm
from .models import Expediente

class ExpedienteForm(ModelForm):
    class Meta:
        model = Expediente
        fields = ['title', 'resumen','importan']
        
#class Registro()