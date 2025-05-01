from datetime import datetime
from django.forms import *
from .models import Expediente, Cliente, Registro


class ExpedienteForm1(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs.update({'autocomplete': 'off'})
        # Ordenar los clientes alfabéticamente por nombre completo
        self.fields['clientes'].queryset = Cliente.objects.all().order_by('nombre', 'apellido')

    class Meta:
        model = Expediente
        fields = ['title', 'fecha_complete', 'clasificacion', 'clientes', 'procedencia', 'ueb_obets', 'reclamacion']
        template_name = 'expedientes/crear.html'
        widgets = {
            'title':TextInput(
                attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese nombre del expediente',
                'autofocus': 'autofocus',  
                }
            ),
            'fecha_complete': DateInput(
                format='%d-%m-%Y',
                attrs={
                    'class': 'form-control',
                    'type': 'date',  # Habilitar el selector de fecha
                    'placeholder': 'Seleccione una fecha',
                }
            ),
            #IMPLEMENTAR MULTIPLES CLIENTES
            'clientes': SelectMultiple(
                attrs={
                    'class': 'form-control select2', 
                    'placeholder': 'Seleccione uno o mas clientes',
                    'style': 'width: 100%;'
                }
            ),
            'clasificacion': Select(
                attrs={
                    'class': 'form-select',
                    'data-placeholder': 'Seleccione una clasificacion',
                    'style': 'width: 100%;',
                    
                    
                }
            ),
            'procedencia': Select(
                attrs={
                    'class': 'form-select',
                    'data-placeholder': 'Seleccione una procedencia',
                    'style': 'width: 100%;'
                }
            ),
            'ueb_obets': Select(
                attrs={
                    'class': 'form-select',
                    'data-placeholder': 'Seleccione la Unidad Base',
                    'style': 'width: 100%;'
                }
            ),
            'reclamacion': Select(
                attrs={
                    'class': 'form-select',
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