from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    # Puedes agregar campos adicionales aquí si es necesario
    rol = models.CharField(max_length=50, choices=[
        ('admin', 'Administrador'),
        ('tecnico', 'Tecnico'),
        ('director', 'Director'),
        ('auditor', 'Auditor')
    ])

    