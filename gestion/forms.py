from datetime import datetime
from django.forms import *
import re
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
        fields = '__all__'
        template_name = 'expedientes/crear.html' #Para que es la propiedad esta
        widgets = {
            'title':TextInput(
                attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese nombre del expediente',
                'autofocus': 'autofocus',  
                }
            ),
            'fecha_entrega': DateInput(
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
            #'archivo': 
            
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
    
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        if not re.match(r'^[A-ZÁÉÍÓÚÑ][a-záéíóúñ\s]*$', nombre):
            raise ValidationError('El nombre debe comenzar con mayúscula y contener solo letras')
        return nombre

    def clean_apellido(self):
        apellido = self.cleaned_data['apellido']
        if not re.match(r'^[A-ZÁÉÍÓÚÑ][a-záéíóúñ\s]*$', apellido):
            raise ValidationError('El apellido debe comenzar con mayúscula y contener solo letras')
        return apellido

    def clean_carnet(self):
        carnet = self.cleaned_data['carnet']
        # Validación para carnet cubano (11 dígitos)
        if not re.match(r'^[0-9]{11}$', carnet):
            raise ValidationError('El carnet debe tener 11 dígitos numéricos')
        return carnet

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        # Validación para teléfono cubano (8 dígitos, opcional +53 al inicio)
        if not re.match(r'^(\+53)?[0-9]{8}$', telefono):
            raise ValidationError('Teléfono inválido. Ejemplo válido: +5351234567 o 51234567')
        return telefono

    def clean_direccion(self):
        direccion = self.cleaned_data['direccion']
        # Permite letras, números, espacios y los caracteres especiales .,/#
        if not re.match(r'^[A-Za-z0-9áéíóúñÁÉÍÓÚÑ\s.,/#]+$', direccion):
            raise ValidationError('La dirección solo puede contener letras, números y los caracteres ., / #')
        return direccion
        
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