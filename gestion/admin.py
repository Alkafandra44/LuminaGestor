from django.contrib import admin
from gestion.models import *;


class ExpedienteAdmin(admin.ModelAdmin):
    readonly_fields = ("fecha_create", )


# Register your models here.
admin.site.register(Expediente, ExpedienteAdmin)

admin.site.register(Procedencia)
admin.site.register(Municipio)
admin.site.register(Cliente)
admin.site.register(Registro)
admin.site.register(Reclamacion)
admin.site.register(DetalleReclamacion)
