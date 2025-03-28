from django.db import models
from django.conf import settings

class BaseModel(models.Model):
    user_creation = models.ForeignKey(settings. AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, blank=True)
    date_update = models.DateTimeField()
    user_update = models.ForeignKey(auto_now=True, blank=True)
     