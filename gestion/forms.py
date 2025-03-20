from django.forms import ModelForm
from .models import Expediente, Cliente


class ExpedienteForm(ModelForm):
    class Meta:
        model = Expediente
        fields = ['title', 'resumen', 'importan']

# class Registro()

#===Muestra los campos del formulario
class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        template_name = 'clientes/crear.html'
