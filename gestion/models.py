from django.db import models
from django.forms import model_to_dict
from datetime import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core import validators
from gestion.choice import * 
from user.models import *

from basemodel import BaseModel

import os
from django.conf import settings # Para acceder a MEDIA_ROOT


#REGISTRO
class Registro(models.Model):
    id_registro = models.AutoField(primary_key=True)
    title = models.CharField(
        max_length=10, 
        unique=True,
        validators=[
            validators.RegexValidator(
                regex=r'^[0-9]{4}$',
                message='El título debe ser un número de 4 dígitos.',
                code='invalid_title'
            )
        ],
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        super().clean()
        # Validar que el título sea único
        if Registro.objects.filter(title=self.title).exclude(pk=self.pk).exists():
            raise ValidationError({'title': 'El título ya existe. Debe ser único.'})

    def save(self, *args, **kwargs):
        # Llama a clean() para realizar las validaciones personalizadas
        self.clean()    
        # Obtener el nombre anterior del registro si existe
        if self.pk:
            old_instance = Registro.objects.get(pk=self.pk)
            old_folder = os.path.join(settings.MEDIA_ROOT, 'registros', old_instance.title)
            new_folder = os.path.join(settings.MEDIA_ROOT, 'registros', self.title)
            # Renombrar la carpeta si el título ha cambiado
            if old_instance.title != self.title and os.path.exists(old_folder):
                os.rename(old_folder, new_folder)
        else:
            # Crear la carpeta si es un nuevo registro
            registro_folder = os.path.join(settings.MEDIA_ROOT, 'registros', self.title)
            if not os.path.exists(registro_folder):
                os.makedirs(registro_folder)
        super().save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        # Eliminar la carpeta del registro
        registro_folder = os.path.join(settings.MEDIA_ROOT, 'registros', self.title)
        if os.path.exists(registro_folder):
            os.rmdir(registro_folder)  # Eliminar la carpeta
        super().delete(*args, **kwargs)
            
    def toJSON(self):
        item = model_to_dict(self)
        item['fecha_creacion'] = self.fecha_creacion.strftime('%d-%m-%Y %H:%M:%S')
        return item
    
    def __str__(self):
        return f"{self.title} {self.fecha_creacion}"
    
 
#MUNICIPIO
class Municipio(models.Model): #no choice
    id_municipio = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)

    def toJSON(self):
        item = model_to_dict(self)
        return item
    
    def __str__(self):
        return self.nombre

#CLIENTE
class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    carnet = models.CharField(max_length=20, unique=True, verbose_name='Cédula')
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    apellido = models.CharField(max_length=100, verbose_name='Apellidos')
    telefono = models.CharField(max_length=15, blank=True, null=True, verbose_name='Teléfono')
    direccion = models.CharField(max_length=150, verbose_name='Dirección')
    is_delete = models.BooleanField(default=False, verbose_name='Eliminado')
    municipio = models.ForeignKey(Municipio, 
        on_delete=models.CASCADE, 
        null=True,
        related_name='clientes', #Permite acceder a todos los clientes de un municipio usando municipio.clientes.all()
        verbose_name='Municipio'
    )
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    def toJSON(self):
        item = model_to_dict(self)
        item['nombre_completo'] = f"{self.nombre} {self.apellido}"
        item['direccion_completa'] = '{} / {}'.format(self.direccion, self.municipio.nombre) 
        item['municipio'] = self.municipio.toJSON()
        return item
    
#DETALLE_RECLAMACION
class DetalleReclamacion(models.Model):
    id_det_recl = models.AutoField(primary_key=True) 
    codigo = models.CharField(
        max_length=4,
        choices=CODIGO,
        default='2105',
        verbose_name="Código"
    )
    def toJSON(self):
        item = model_to_dict(self)
        return item
    
    def __str__(self):
        return self.codigo
    
#RECLAMACION
class Reclamacion(models.Model):
    id_reclamacion = models.AutoField(primary_key=True)
    descripcion = models.CharField(
        max_length=100, 
        unique=True,
        choices=RECLAMACION,
        default='Lineas y Postes',
        verbose_name="Reclamacion"
    )
    detalle_reclamacion = models.ForeignKey(
        DetalleReclamacion,
        on_delete=models.CASCADE,
        related_name='reclamaciones',
        verbose_name="Detalle de Reclamación"
    )
    def toJSON(self):
        item = model_to_dict(self)
        return item
    
    def __str__(self):
        return self.descripcion
  
    
#ARCHIVOS
class Archivo(models.Model):
    id_archivo = models.AutoField(primary_key=True)
    archivo = models.FileField(upload_to='expedientes/archivos/%Y/%m/%d/')
    nombre = models.CharField(max_length=255, verbose_name = "Nombre del Archivo")
    fecha_create = models.DateTimeField(auto_now_add=True, verbose_name ="Fecha de Creación")
    expediente = models.ForeignKey(
        'Expediente',
        on_delete=models.CASCADE,
        related_name='archivos',
        verbose_name="Archivos"
    )
    def toJSON(self):
        item = model_to_dict(self)
        return item
    
    def __str__(self):
        return self.nombre
    
#PROCEDENCIA
class Procedencia(models.Model): #no Choice
    id_procedencia = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50,unique=True)
    
    def toJSON(self):
        item = model_to_dict(self)
        return item
    
    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name = 'Procedencia'
        verbose_name_plural = 'Procedencias'
        ordering = ['id_procedencia']
         
#ESTADO_EXPEDIENTE
class EstadoExpediente(models.Model): #no Choice
    id_estado = models.AutoField(primary_key=True)
    estado = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Estado"
    )

    def toJSON(self):
        item = model_to_dict(self)
        return item
    
    def __str__(self):
        return self.estado

    
#EXPEDIENTE
class Expediente(models.Model):
    id_expediente = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, default='')
    resumen = models.TextField(blank=True, null=True)
    fecha_create = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateField(null=True)
    estado_expediente = models.ForeignKey(
        EstadoExpediente,
        on_delete=models.PROTECT,
        related_name='expedientes',
        verbose_name="Estado",
        default=1 
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    clientes = models.ManyToManyField(
        'Cliente', 
        related_name='expedientes',
    )
    registro = models.ForeignKey(
        'Registro', 
        on_delete=models.PROTECT,
        related_name='expedientes',
        verbose_name="Registro Anual"
    )
    clasificacion = models.CharField(
        max_length=50,
        choices=Clasificacion,
        verbose_name="Clasificación"
    )
    procedencia = models.ForeignKey(
        Procedencia, 
        on_delete=models.CASCADE, 
        related_name='expedientes', 
        verbose_name="Procedencia"
    )
    ueb_obets = models.CharField(
        max_length=50,
        choices=UEB_OBTs,
        default='UEB_Calimete',
        verbose_name="Unidad Empresarial de Base",
    )
    reclamacion = models.ForeignKey(
    Reclamacion,
    on_delete=models.CASCADE,
    related_name='expedientes',
    verbose_name="Reclamación Asociada"
    )
    
    def save(self, *args, **kwargs):
        # Determinar si es un nuevo expediente
        is_new = self.pk is None
        # Obtener los datos antiguos si es una edición
        if not is_new:
            old_instance = Expediente.objects.get(pk=self.pk)
            old_id = old_instance.id_expediente
            old_title = old_instance.title
        else:
            old_id = None
            old_title = None
        super().save(*args, **kwargs)
        
        # Crear o renombrar la carpeta asociada al expediente
        registro_folder = os.path.join(settings.MEDIA_ROOT, 'registros', self.registro.title)
        expediente_folder = os.path.join(registro_folder, f"{str(self.id_expediente).zfill(3)}_{self.title}")
        
        if is_new:
            # Crear la carpeta después de guardar (id_expediente ya existe)
            if not os.path.exists(expediente_folder):
                os.makedirs(expediente_folder)
            else:
                # Verificar si cambió el id_expediente o el título para renombrar
                new_id = self.id_expediente
                new_title = self.title
                old_folder_path = os.path.join(registro_folder, f"{str(old_id).zfill(3)}_{old_title}")
            
                if (old_id != new_id) or (old_title != new_title):
                    if os.path.exists(old_folder_path):
                        os.rename(old_folder_path, expediente_folder)

    # def delete(self, *args, **kwargs):
    #     # Eliminar la carpeta asociada al expediente
    #     registro_folder = os.path.join(settings.MEDIA_ROOT, 'registros', self.registro.title)
    #     expediente_folder = os.path.join(registro_folder, f"{str(self.id_expediente).zfill(3)}_{self.title}")
    #     if os.path.exists(expediente_folder):
    #         os.rmdir(expediente_folder)  # Eliminar la carpeta
    #     super().delete(*args, **kwargs)

    def toJSON(self):
        item = model_to_dict(self, exclude=['clientes'])
                
        expediente = Expediente.objects.prefetch_related('clientes').get(pk=self.pk)
        # Convertir campos ManyToMany a una lista de diccionarios
        item['clientes'] = [{
            'id_cliente': c.id_cliente, 
            'nombre_completo': f"{c.nombre} {c.apellido}",
            'carnet': c.carnet,
            'municipio': c.municipio.nombre if c.municipio else None
            } for c in expediente.clientes.all()
        ]
        
        item['id_expediente'] = self.id_expediente
        # Convertir campos ForeignKey a diccionarios completos (opcional)
        item['user'] = {'id': self.user.id, 'username': self.user.username}
        item['title'] = self.title
        item['registro'] = {'id_registro': self.registro.pk, 'title': self.registro.title}
        item['procedencia'] = model_to_dict(self.procedencia)
        item['estado_expediente'] = model_to_dict(self.estado_expediente)
        item['clasificacion'] = self.get_clasificacion_display() if hasattr(self, 'get_clasificacion_display') else self.clasificacion
        item['reclamacion'] = str(self.reclamacion) if self.reclamacion else ''
        item['estado_expediente'] = str(self.estado_expediente) if self.estado_expediente else ''

        # Formatear fechas para que sean JSON-serializables
        item['fecha_create'] = self.fecha_create.strftime("%d/%m/%Y") if self.fecha_entrega else "No especificado"
        item['fecha_entrega'] = self.fecha_entrega.strftime("%d/%m/%Y") if self.fecha_entrega else "No especificado"
        
        return item
    
    def __str__(self):
        numero_expediente = str(self.id_expediente).zfill(3)
        return f"{numero_expediente} {self.title} - by {self.user.username}"

class RespuestaCliente(models.Model):
<<<<<<< HEAD
    expediente = models.ForeignKey(
        Expediente, 
        on_delete=models.CASCADE,
        related_name='respuesta',
        verbose_name="Respuestas"
        )
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    respuesta = models.TextField()
    fecha_respuesta = models.DateTimeField(auto_now_add=True)
    evaluacion_gestion = models.CharField(
        max_length=50,
        choices=Evaluacion_gestion,
        verbose_name="Evaluación de la Gestión",
        blank=True, 
        null=True
    )
    resultado_gestion = models.CharField(
        max_length=50,
        choices=Resultado_de_la_gestion,
        verbose_name="Resultado de la Gestión",
        blank=True, 
        null=True
    )
    
    def __str__(self):
        return f"Respuesta de {self.cliente} para expediente {self.expediente} - {self.fecha_respuesta.strftime('%d/%m/%Y')}"
        
    def toJSON(self):
        item = model_to_dict(self)
        item['expediente'] = self.expediente.toJSON()
        item['cliente'] = self.cliente.toJSON()
        item['fecha_respuesta'] = self.fecha_respuesta.strftime('%d-%m-%Y %H:%M:%S')
        return item
    
=======
    expediente = models.ForeignKey(Expediente, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    respuesta = models.TextField()
    fecha_respuesta = models.DateTimeField(auto_now_add=True)
>>>>>>> ecfc6af31397f7a9ac011b9197ad1562a49f381b
