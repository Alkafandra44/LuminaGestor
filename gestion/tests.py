from django.test import TestCase
from .models import Municipio

# Create your tests here.


#LISTAR MUNICIPIOS==============
# query = Municipio.objects.all()
# print(query)

#INSERTAR SIMPLE===============
#mun = Municipio(nombre='Matanzas').save()

#INSERTAR MULTIPLE==========

# municipios = [
#     #Municipio(nombre="Limonar"),
#    # Municipio(nombre="Cárdenas"),
#     #Municipio(nombre="Colón"),
#     Municipio(nombre="Jovellanos"),
#     Municipio(nombre="Cienaga de Zapata"),
#     Municipio(nombre="Unión de Reyes"),
#     Municipio(nombre="Perico"),
#     Municipio(nombre="Los Arabos"),
#     Municipio(nombre="Jaguey Grande"),
#     Municipio(nombre="Martí"),
#     Municipio(nombre="Calimete"),
#     Municipio(nombre="Pedro Betancourt"),
 
#     # Agrega todos los municipios necesarios
#]
#Municipio.objects.bulk_create(municipios)

#MOSTRAR REGISTRO EN LA TABLA
m = Municipio.objects.get(id_municipio=1)
print(m.nombre)