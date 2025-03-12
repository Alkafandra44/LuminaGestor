from django.contrib import admin
from .models import Expediente, Registro;


class ExpedienteAdmin(admin.ModelAdmin):
    readonly_fields = ("fecha_create", )


# Register your models here.
admin.site.register(Expediente, ExpedienteAdmin)
