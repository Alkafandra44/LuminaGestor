# Generated by Django 5.1.7 on 2025-03-13 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0004_clasificacion_detallereclamacion_estadoexpediente_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='procedencia',
            name='nombre',
            field=models.CharField(default=0, max_length=50, unique=True),
            preserve_default=False,
        ),
    ]
