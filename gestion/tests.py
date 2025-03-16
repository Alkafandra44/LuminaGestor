from django.test import TestCase
from .models import Municipio, Cliente

class ClienteTestCase(TestCase):
    def setUp(self):
        # Crear un municipio para asignar a los clientes
        self.municipio = Municipio.objects.create(nombre="Municipio de Prueba")

    def test_crear_clientes(self):
        # Crear instancias de Cliente
        cliente1 = Cliente(
            carnet="123456789",
            nombre="Juan",
            apellido="Pérez",
            telefono="123456789",
            direccion="Calle Falsa 123",
            municipio=self.municipio
        )
        cliente2 = Cliente(
            carnet="987654321",
            nombre="Ana",
            apellido="Gómez",
            telefono="987654321",
            direccion="Avenida Siempre Viva 742",
            municipio=self.municipio
        )

        # Guardar los clientes
        cliente1.save()
        cliente2.save()

        # Verificar que los clientes se han guardado correctamente
        self.assertEqual(Cliente.objects.count(), 2)
        self.assertEqual(Cliente.objects.get(carnet="123456789").nombre, "Juan")
        self.assertEqual(Cliente.objects.get(carnet="987654321").nombre, "Ana")
