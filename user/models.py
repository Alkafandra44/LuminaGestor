from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    img = models.ImageField(upload_to='users/%m/%d/%Y', blank=True, null=True)  
    
    def get_img(self):
        if self.img:
            return self.img.url
        return '/media/users/default.jpg'