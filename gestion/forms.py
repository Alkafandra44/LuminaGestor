from django.forms import *
from .models import Expediente, Cliente


class ExpedienteForm(ModelForm):
    class Meta:
        model = Expediente
        fields = ['title', 'resumen', 'importan']

# class Registro()

#===Muestra los campos del formulario
class ClienteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})

    class Meta:
        model = Cliente
        fields = '__all__'
        template_name = 'clientes/crear.html'
        
        widgets = {
            'carnet': TextInput(
                attrs={
                'placeholder': 'Ingrese carnet de identidad',
                'autofocus': 'autofocus',  # Agregar autofocus aquí
                }
            ),
            'direccion': Textarea(
                attrs={
                    'rows': 2,
                    'cols': 2
                }
            )
        }
        
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
