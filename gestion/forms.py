from datetime import datetime
from django.forms import *
from .models import Expediente, Cliente, Registro


class ExpedienteForm1(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})
    class Meta:
        model = Expediente
        fields = ['title', 'fecha_complete', 'clasificacion', 'clientes', 'procedencia', 'ueb_obets', 'reclamacion']
        template_name = 'expedientes/crear.html'
        widgets = {
            'title':TextInput(
                attrs={
                'placeholder': 'Ingrese nombre del expediente',
                'autofocus': 'autofocus',  # Agregar autofocus aquí
                }
            ),
            'fecha_complete': DateInput(format='%d-%m-%Y',
                attrs={
                    'data-placeholder': 'Seleccione fecha de entrega',
                    'style': 'width: 100%;',
                    'value': datetime.now().strftime('%d-%m-%Y'),
                }
            ),
            #IMPLEMENTAR MULTIPLES CLIENTES
            'clientes': Select(
                attrs={
                    #'class': 'form-control select2',
                    'data-placeholder': 'Seleccione un cliente',
                    'style': 'width: 100%;'
                }
            ),
            'clasificacion': Select(
                attrs={
                    #'class': 'form-control select2',
                    'data-placeholder': 'Seleccione una clasificacion',
                    'style': 'width: 100%;'
                }
            ),
            'procedencia': Select(
                attrs={
                    #'class': 'form-control select2',
                    'data-placeholder': 'Seleccione una procedencia',
                    'style': 'width: 100%;'
                }
            ),
            'ueb_obets': Select(
                attrs={
                    #'class': 'form-control select2',
                    'data-placeholder': 'Seleccione la Unidad Base',
                    'style': 'width: 100%;'
                }
            ),
            'reclamacion': Select(
                attrs={
                    #'class': 'form-control select2',
                    'data-placeholder': 'Seleccione el tipo de reclamacion',
                    'style': 'width: 100%;'
                }
            ),
            
        }

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
   
class RegistroForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})
    class Meta:
        model = Registro
        fields = ['title']
        widgets = {
            'title': TextInput(
                attrs={
                'placeholder': 'Título del registro'
                }
            ),
        }