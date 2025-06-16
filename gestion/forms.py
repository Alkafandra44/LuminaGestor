from datetime import date, datetime
from django.forms import *
import re
from .models import EstadoExpediente, Expediente, Cliente, Registro, RespuestaCliente, Archivo

class MultipleFileInput(ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result
class ExpedienteForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        self.fields['estado_expediente'].required = False
        
        for form in self.visible_fields():
            form.field.widget.attrs.update({'autocomplete': 'off'})
            
        # Forzar el valor inicial en el widget para edición
        if self.instance and self.instance.pk and self.instance.fecha_entrega:
            fecha_str = self.instance.fecha_entrega.strftime('%d-%m-%Y')
            self.initial['fecha_entrega'] = fecha_str
            
        # Ordenar los clientes alfabéticamente por nombre completo
        self.fields['clientes'].queryset = Cliente.objects.all().order_by('nombre', 'apellido')
        if not self.instance.pk and not self.fields['estado_expediente'].initial:
            try:
                self.fields['estado_expediente'].initial = EstadoExpediente.objects.get(estado='Pendiente').pk
            except EstadoExpediente.DoesNotExist:
                pass
        # Si se especifican campos, elimina los que no estén en la lista
        if fields is not None:
            allowed = set(fields)
            for field_name in list(self.fields.keys()):
                if field_name not in allowed:
                    self.fields.pop(field_name)
                    
    fecha_entrega = DateField(
        input_formats=['%d-%m-%Y'],
        widget=DateInput(
            format='%d-%m-%Y',
            attrs={
                'class': 'form-control datetimepicker-input form-control-sm',
                'id': 'fecha_entrega',
                'data-target': '#fecha_entrega',
                'data-toggle': 'datetimepicker',
                'placeholder': 'Seleccione una fecha',
            }
        )
    )
    archivos = MultipleFileField(
        required=False,
        label="Subir archivos",
        widget=MultipleFileInput(
            attrs={
            'class': 'form-control form-control-sm',
            'accept': '.pdf,.doc,.docx,.xls,.xlsx,.jpg,.png',
            }
        )
    )

    class Meta:
        model = Expediente
        fields = '__all__'
        exclude = ['user']
        template_name = 'expedientes/crear.html' #Para que es la propiedad esta
        widgets = {
            'title':TextInput(
                attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Ingrese nombre del expediente',
                'autofocus': 'autofocus',  
                }
            ),
            #IMPLEMENTAR MULTIPLES CLIENTES
            'clientes': SelectMultiple(
                attrs={
                    'class': 'form-control select2 form-select-sm', 
                    'style': 'width: 100%;',
                    'placeholder': 'Seleccione uno o mas clientes',
                }
            ),
            'clasificacion': Select(
                attrs={
                    'class': 'form-control form-select-sm',
                    'style': 'width: 100%;',
                    'placeholder': 'Seleccione una clasificacion',
                }
            ),
            'procedencia': Select(
                attrs={
                    'class': 'form-control form-select-sm',
                    'style': 'width: 100%;',
                    'placeholder': 'Seleccione una procedencia',
                }
            ),
            'ueb_obets': Select(
                attrs={
                    'class': 'form-control form-select-sm',
                    'style': 'width: 100%;',
                    'placeholder': 'Seleccione la Unidad Base',
                }
            ),
            'reclamacion': Select(
                attrs={
                    'class': 'form-control form-select-sm',
                    'style': 'width: 100%;',
                    'placeholder': 'Seleccione el tipo de reclamacion',
                }
            ),
            'resumen': Textarea(
                attrs={
                    'class': 'form-control form-control-sm',
                    'rows': 2,                    
                    'style': 'width: 100%;',
                    'placeholder': 'Resumen del caso',
                }
            ),
        }
        
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise ValidationError("El título debe tener al menos 5 caracteres")
        if not re.match(r'^[A-ZÁÉÍÓÚÑ]', title):
            raise ValidationError("El título debe comenzar con mayúscula")
        return title
    
    def clean_fecha_entrega(self):
        fecha = self.cleaned_data.get('fecha_entrega')
        return fecha

    def clean_resumen(self):
        resumen = self.cleaned_data['resumen']
        if len(resumen) > 0 and len(resumen) < 20:  # Opcional pero no vacío
            raise ValidationError("El resumen debe tener al menos 20 caracteres")
        return resumen
    
    def clean_clientes(self):
        clientes = self.cleaned_data['clientes']
        if not clientes.exists():
            raise ValidationError("Debe seleccionar al menos un cliente")
        return clientes
    
    def clean_archivos(self):
        archivos = self.cleaned_data.get('archivos', [])
        if not archivos:
            return[]
        
        for archivo in archivos:
            if archivo.size > 10 * 1024 * 1024:  # 10MB límite
                raise ValidationError("El archivo {} excede el tamaño máximo permitido (10MB)".format(archivo.name))
        return archivos
    
class RespuestaClienteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.expediente = kwargs.pop('expediente', None)
        cliente = kwargs.pop('cliente', None)
        super().__init__(*args, **kwargs)
        
        for formresp in self.visible_fields():
            formresp.field.widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})
            
        if self.expediente:
            self.fields['cliente'].initial = cliente.id_cliente
            
        if cliente:
            self.fields['cliente'].initial = cliente.cliente_id
        
    class Meta:
        model = RespuestaCliente
        fields = ['cliente', 'respuesta', 'evaluacion_gestion', 'resultado_gestion' ]
        exclude = ['estado']
        widgets = {
            'cliente': Select(
                attrs={
                    'class': 'form-control form-select-sm',
                    'style': 'width: 100%;',
                    'placeholder': 'Seleccione un cliente',
                }
            ),
            'respuesta': Textarea(
                attrs={
                    'class': 'form-control form-control-sm',
                    'rows': 3,
                    'placeholder': 'Redacte la respuesta para el cliente'
                }
            ),
            'evaluacion_gestion': Select(
                attrs={
                    'class': 'form-control form-select-sm',
                    'style': 'width: 100%;',
                    'placeholder': 'Seleccione la evaluacion final',
                }
            ),
            'resultado_gestion': Select(
                attrs={
                    'class': 'form-control form-select-sm',
                    'style': 'width: 100%;',
                    'placeholder': 'Seleccione la evaluacion final',
                }
            ),
        }

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