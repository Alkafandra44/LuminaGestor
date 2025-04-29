from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import model_to_dict

# Create your models here.
class User(AbstractUser):
    # Puedes agregar campos adicionales aquí si es necesario
    rol = models.CharField(max_length=50, choices=[
        ('admin', 'Administrador'),
        ('tecnico', 'Tecnico'),
        ('director', 'Director'),
        ('auditor', 'Auditor')
    ])
    
    def toJSON(self):
        item = model_to_dict(self, exclude=['password', 'last_login', 'user_permissions'])
        if self.last_login:
            item['last_login'] = self.last_login.strftime('%d/%m/%Y')
        item['date_joined'] = self.date_joined.strftime('%d/%m/%Y')
        return item
    
