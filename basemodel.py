from django.db import models

class BaseModel(models.Model):
    user_creation = models.ForeignKey()
    date_creation = models.DateTimeField(auto_now_add=True, blank=True)
    date_update = models.DateTimeField()
    user_update = models.ForeignKey(auto_now=True, blank=True)
     