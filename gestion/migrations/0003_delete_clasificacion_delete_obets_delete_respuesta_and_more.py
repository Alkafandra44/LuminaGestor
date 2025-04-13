# Generated by Django 5.1.7 on 2025-04-05 04:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0002_expediente_date_creation_expediente_date_update_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Clasificacion',
        ),
        migrations.DeleteModel(
            name='Obets',
        ),
        migrations.DeleteModel(
            name='Respuesta',
        ),
        migrations.DeleteModel(
            name='Resultado',
        ),
        migrations.AddField(
            model_name='expediente',
            name='clasificacion',
            field=models.CharField(choices=[('solicitud', 'Solicitud'), ('queja', 'Queja'), ('sugerencia', 'Sugerencia'), ('denuncia', 'Denuncia')], default='queja', max_length=50, verbose_name='Clasificación'),
        ),
        migrations.AddField(
            model_name='expediente',
            name='evaluacion_gestion',
            field=models.CharField(choices=[('solucionado', 'Solucionado'), ('pendiente_a_solucion', 'Pendiente a Solucion'), ('sin_solucion', 'Sin Solucion'), ('no_procede', 'No Procede')], default='solucionado', max_length=50, verbose_name='Evaluación de la Gestión'),
        ),
        migrations.AddField(
            model_name='expediente',
            name='procedencia',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, related_name='expedientes', to='gestion.procedencia', verbose_name='Procedencia'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='expediente',
            name='respuesta',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='expediente',
            name='ueb_obets',
            field=models.CharField(choices=[('UEB_Calimete', 'Unidad Empresarial de Base Calimete'), ('UEB2_Cárdenas', 'Unidad Empresarial de Base Cárdenas'), ('UEB3_Cienaga', 'Unidad Empresarial de Base Cienaga de Zapata'), ('UEB4_Colón', 'Unidad Empresarial de Base Colón'), ('UEB5_Jaguey', 'Unidad Empresarial de Base Jaguey Grande'), ('UEB6_Jovellanos', 'Unidad Empresarial de Base Jovellanos'), ('UEB7_Limonar', 'Unidad Empresarial de Base Limonar'), ('UEB8_Arabos', 'Unidad Empresarial de Base Los Arabos'), ('UEB9_Martí', 'Unidad Empresarial de Base Martí'), ('UEB10_Matanzas', 'Unidad Empresarial de Base Matanzas'), ('UEB11_Pedro_B', 'Unidad Empresarial de Base Pedro Betancourt'), ('UEB12_Perico', 'Unidad Empresarial de Base Perico'), ('UEB13_Unión', 'Unidad Empresarial de Base Unión de Reyes')], default='UEB_Matanzas', max_length=50, verbose_name='Unidad Empresarial de Base'),
        ),
        migrations.AlterField(
            model_name='expediente',
            name='registro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='expedientes', to='gestion.registro', verbose_name='Registro Anual'),
        ),
    ]
