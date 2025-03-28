from django.db import models
from django.forms import model_to_dict
from datetime import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

import os
from django.conf import settings # Para acceder a MEDIA_ROOT

# Create your models here.
class Expediente(models.Model):
    id_expediente = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, default='')
    resumen = models.TextField(blank=True)
    fecha_create = models.DateTimeField(auto_now_add=True)
    fecha_complete = models.DateTimeField(null=True)
    importan = models.BooleanField(default=False)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    clientes = models.ManyToManyField(
        'Cliente', 
        related_name='expedientes'
        )
    registro = models.ForeignKey(
        'Registro', 
        on_delete=models.CASCADE, #no borrar registro si tiene expedientes con menos de 5 years.
        related_name='expedientes',
        verbose_name="Registro Anual"
    )
    #AGREGAR LOS SIGUIENTES CAMPOS A LA TABLA EXPEDIENTE
    #respuesta, FK cliente, *FK Registro*, FK detalles_archivos, FK respuesta, FK detalles_reclamacion, FK procedencia, FK ueb_obets, FK clasificacion, FK estado_expediente, 
    
    def __str__(self):
        numero_expediente = str(self.id_expediente).zfill(3)
        return f"{numero_expediente} {self.title} - by {self.user.username}"
    
    #REGISTRO
class Registro(models.Model):
    id_registro = models.AutoField(primary_key=True)
    title = models.CharField(max_length=10)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
        
    def save(self, *args, **kwargs):
        self.clean()  # Llamar a la validación antes de guardar
        super().save(*args, **kwargs)
        # Crear una carpeta con el nombre del registro
        registro_folder = os.path.join(settings.MEDIA_ROOT, 'registros', self.title)
        if not os.path.exists(registro_folder):
            os.makedirs(registro_folder)
    
    def __str__(self):
        return f"{self.title} {self.fecha_creacion} - by {self.user.username}"
    
    #CLIENTE
class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    carnet = models.CharField(max_length=20, unique=True, verbose_name='Cédula')
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    apellido = models.CharField(max_length=100, verbose_name='Apellidos')
    telefono = models.CharField(max_length=15, blank=True, null=True, verbose_name='Teléfono')
    direccion = models.CharField(max_length=150, verbose_name='Dirección')
    municipio = models.ForeignKey(
        'Municipio', 
        on_delete=models.SET_NULL, 
        default=1, 
        null=True,
        blank=True, 
        related_name='clientes', #Permite acceder a todos los clientes de un municipio usando municipio.clientes.all()
        verbose_name='Municipio'
    )
    def __str__(self):
        return self.nombre
    
    def toJSON(self):
        item = model_to_dict(self)
        # print(item)
        return item
    
    #MUNICIPIO
class Municipio(models.Model):
    id_municipio = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre
    
    
    #RECLAMACION
class Reclamacion(models.Model):
    id_reclamacion = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100, unique=True)
    
    
    #DETALLE_RECLAMACION
class DetalleReclamacion(models.Model):
    id_det_recl = models.AutoField(primary_key=True) 
    CODIGO = [
        #('2105', 'Operaciones'),
        #('2103', 'Operaciones'),
        #('2106', 'Comercial'),
        #('2101', 'Operaciones'),
        #('2104', 'Daño a la Propiedad'),
        #('2105', 'Operaciones'),
    ]  
    
    #ARCHIVOS
class Archivo(models.Model):
    TIPO_ARCHIVO = [
        #('doc', 'Documento Word'),
        #('pdf', 'Documento PDF'),
        #('img', 'Imagen'),
        #('word', 'Documento Word'),
        #('otro', 'Otro formato'),
    ]
    id_archivo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, verbose_name = "Nombre del Archivo"),
    fecha_create = models.DateTimeField(auto_now_add=True, verbose_name ="Fecha de Creación")
    expediente = models.ForeignKey(
        'Expediente',
        on_delete=models.CASCADE,
        related_name='archivos',
        verbose_name="Expediente Asociado"
    )

    #PROCEDENCIA
class Procedencia(models.Model):
    id_procedencia = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50,unique=True)
    
    def __str__(self):
        return self.nombre
    
    #RESUESTA    
class Respuesta(models.Model):
    id_respuesta = models.AutoField(primary_key=True)   
    
    #RESULTADO
class Resultado(models.Model):
    id_resultado = models.AutoField(primary_key=True)    
    
    #EVALUACION_DE_LA_GESTION
    
    #UEB OBETs
class Obets(models.Model):
    id_obet = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50,unique=True)
        
    
    #CLASIFICACION
class Clasificacion(models.Model):
    id_clasificacion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50,unique=True)
        
    
    #ESTADO_EXPEDIENTE
class EstadoExpediente(models.Model):
    id_archivo = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=50,unique=True)
    
    
    
    #1. ESTABLECER SUS RELACIONES