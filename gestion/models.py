from django.db import models
from django.forms import model_to_dict
from datetime import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core import validators

from basemodel import BaseModel

import os
from django.conf import settings # Para acceder a MEDIA_ROOT

# Create your models here.
   
#REGISTRO
class Registro(models.Model):
    id_registro = models.AutoField(primary_key=True)
    title = models.CharField(max_length=10, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
         
    def save(self, *args, **kwargs):
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
    municipio = models.ForeignKey(Municipio, 
        on_delete=models.SET_NULL, 
        default=1, 
        null=True,
        related_name='clientes', #Permite acceder a todos los clientes de un municipio usando municipio.clientes.all()
        verbose_name='Municipio'
    )
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    def toJSON(self):
        item = model_to_dict(self)
        item['nombre_completo'] = f"{self.nombre} {self.apellido}"
        item['municipio'] = self.municipio.nombre
        return item
 
      
#RECLAMACION
class Reclamacion(models.Model):
    id_reclamacion = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100, unique=True)
    detalle_reclamacion = models.ForeignKey(
        'DetalleReclamacion',
        on_delete=models.CASCADE,
        related_name='reclamaciones',
        verbose_name="Detalle de Reclamación"
    )
    def toJSON(self):
        item = model_to_dict(self)
        return item
    
    def __str__(self):
        return self.descripcion
     
#DETALLE_RECLAMACION
class DetalleReclamacion(models.Model):
    id_det_recl = models.AutoField(primary_key=True) 
    CODIGO = [
        ('2105', 'Operaciones'),
        ('2103', 'Operaciones'),
        ('2106', 'Comercial'),
        ('2101', 'Operaciones'),
        ('2104', 'Daño a la Propiedad'),
        ('2105', 'Operaciones'),
    ]
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
    nombre = models.CharField(max_length=255, verbose_name = "Nombre del Archivo")
    fecha_create = models.DateTimeField(auto_now_add=True, verbose_name ="Fecha de Creación")
    expediente = models.ForeignKey(
        'Expediente',
        on_delete=models.CASCADE,
        related_name='archivos',
        verbose_name="Expediente Asociado"
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
    estado = models.CharField(max_length=50,unique=True)

    def toJSON(self):
        item = model_to_dict(self)
        return item
    
    def __str__(self):
        return self.estado
    
#EXPEDIENTE
class Expediente(models.Model):
    id_expediente = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, default='')
    resumen = models.TextField(blank=True)
    fecha_create = models.DateTimeField(auto_now_add=True)
    fecha_complete = models.DateTimeField(null=True)
    respuesta = models.TextField(blank=True)
    importan = models.BooleanField(default=False)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
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
    Clasificacion =[
        ('solicitud', 'Solicitud'),
        ('queja', 'Queja'),
        ('sugerencia', 'Sugerencia'),
        ('denuncia', 'Denuncia'),
    ]
    clasificacion = models.CharField(
        max_length=50,
        choices=Clasificacion,
        default='queja',
        verbose_name="Clasificación"
    )
    procedencia = models.ForeignKey(Procedencia, on_delete=models.CASCADE, related_name='expedientes', verbose_name="Procedencia")
    UEB_OBTs =[
        ('UEB_Calimete', 'UEB Calimete'),
        ('UEB2_Cárdenas', 'Unidad Empresarial de Base Cárdenas'),
        ('UEB3_Cienaga', 'Unidad Empresarial de Base Cienaga de Zapata'),
        ('UEB4_Colón', 'Unidad Empresarial de Base Colón'),
        ('UEB5_Jaguey', 'Unidad Empresarial de Base Jaguey Grande'),
        ('UEB6_Jovellanos', 'Unidad Empresarial de Base Jovellanos'),
        ('UEB7_Limonar', 'Unidad Empresarial de Base Limonar'),
        ('UEB8_Arabos', 'Unidad Empresarial de Base Los Arabos'),
        ('UEB9_Martí', 'Unidad Empresarial de Base Martí'),
        ('UEB10_Matanzas', 'Unidad Empresarial de Base Matanzas'),
        ('UEB11_Pedro_B', 'Unidad Empresarial de Base Pedro Betancourt'),
        ('UEB12_Perico', 'Unidad Empresarial de Base Perico'),
        ('UEB13_Unión', 'Unidad Empresarial de Base Unión de Reyes'),
    ]
    ueb_obets = models.CharField(
        max_length=50,
        choices=UEB_OBTs,
        default='UEB_Matanzas',
        verbose_name="Unidad Empresarial de Base"
    )
    Evaluacion_gestion = [
        ('solucionado', 'Solucionado'),
        ('pendiente_a_solucion', 'Pendiente a Solucion'),
        ('sin_solucion', 'Sin Solucion'),
        ('no_procede', 'No Procede'),
    ]
    evaluacion_gestion = models.CharField(
        max_length=50,
        choices=Evaluacion_gestion,
        default='solucionado',
        verbose_name="Evaluación de la Gestión"
    )
    Resultado_de_la_gestion = [
        ('con_razon', 'Con Razón'),
        ('razon_en_parte', 'Razón en Parte'),
        ('sin_razon', 'Sin Razón'),
    ]
    resultado_gestion = models.CharField(
        max_length=50,
        choices=Resultado_de_la_gestion,
        default='con_razon',
        verbose_name="Resultado de la Gestión"
    )
    estado_expediente = models.ForeignKey(
        'EstadoExpediente',
        on_delete=models.PROTECT,
        related_name='expedientes',
        verbose_name="Estado Expediente"
    )
    reclamacion = models.ForeignKey(
    'Reclamacion',
    on_delete=models.CASCADE,
    related_name='expedientes',
    verbose_name="Reclamación Asociada"
    )
    
    def save(self, *args, **kwargs):
        # Crear o renombrar la carpeta asociada al expediente
        registro_folder = os.path.join(settings.MEDIA_ROOT, 'registros', self.registro.title)
        expediente_folder = os.path.join(registro_folder, f"{str(self.id_expediente).zfill(3)}_{self.title}")

        if self.pk:  # Si el expediente ya existe (es una edición)
            old_instance = Expediente.objects.get(pk=self.pk)
            old_folder = os.path.join(registro_folder, f"{str(old_instance.id_expediente).zfill(3)}_{old_instance.title}")
            if old_instance.title != self.title and os.path.exists(old_folder):
                os.rename(old_folder, expediente_folder)  # Renombrar la carpeta si el título cambió
        else:  # Si es un nuevo expediente
            if not os.path.exists(expediente_folder):
                os.makedirs(expediente_folder)  # Crear la carpeta

        super().save(*args, **kwargs)  # Guardar el objeto en la base de datos

    def delete(self, *args, **kwargs):
        # Eliminar la carpeta asociada al expediente
        registro_folder = os.path.join(settings.MEDIA_ROOT, 'registros', self.registro.title)
        expediente_folder = os.path.join(registro_folder, f"{str(self.id_expediente).zfill(3)}_{self.title}")
        if os.path.exists(expediente_folder):
            os.rmdir(expediente_folder)  # Eliminar la carpeta
        super().delete(*args, **kwargs)

    def toJSON(self):
        item = model_to_dict(self)
        return item
    
    def __str__(self):
        numero_expediente = str(self.id_expediente).zfill(3)
        return f"{numero_expediente} {self.title} - by {self.user.username}"
 