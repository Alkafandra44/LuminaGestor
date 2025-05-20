from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import model_to_dict

# Create your models here.
class User(AbstractUser):
    # Puedes agregar campos adicionales aquí si es necesario
        
    def toJSON(self):
        item = model_to_dict(self, exclude=['password', 'last_login', 'user_permissions'])
        if self.last_login:
            item['last_login'] = self.last_login.strftime('%d/%m/%Y')
        item['date_joined'] = self.date_joined.strftime('%d/%m/%Y')
        item['full_name'] = self.get_full_name()
        item['groups'] = [{'id': g.id, 'name': g.name} for g in self.groups.all()]
        return item
    
