from django.views.generic import TemplateView
from django.urls import reverse_lazy
from datetime import datetime
from django.db.models import Count, Case, When, IntegerField

from gestion.models import Expediente, Registro

class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'
    
    def get_queryset(self):
        registro_id = self.request.GET.get('registro')
        qs = Expediente.objects.all()
        if registro_id:
            qs = qs.filter(registro_id=registro_id)
        return qs
    
    # Método para contar expedientes por estado
    def get_counts_by_status(self, qs):
        # Una sola consulta para todos los contadores
        return qs.aggregate(
            total=Count('id_expediente'),
            pendientes=Count(
                Case(
                    When(estado_expediente__estado='Pendiente', then=1),
                    output_field=IntegerField()
                )
            ),
            investigacion=Count(
                Case(
                    When(estado_expediente__estado='Investigación', then=1),
                    output_field=IntegerField()
                )
            ),
            solucionados=Count(
                Case(
                    When(estado_expediente__estado='Solucionado', then=1),
                    output_field=IntegerField()
                )
            ),corregir=Count(
                Case(
                    When(estado_expediente__estado='Corregir', then=1),
                    output_field=IntegerField()
                )
            )
        )
    
    # Método para gráfica de barras
    def get_graf_quejas_mes(self, qs):
        year = datetime.now().year
        expediente_por_mes = []
        for mes in range(1, 13):
            count = qs.filter(
                fecha_create__year=year, 
                fecha_create__month=mes
            ).count()
            expediente_por_mes.append(count)
        return expediente_por_mes
    
    def get_reclamaciones_data(self, qs):
        # Agrupa por reclamación y cuenta expedientes
        qs_grouped = (
            qs.values('reclamacion__descripcion')
            .annotate(total=Count('id_expediente'))
            .order_by('-total')
        )
        # Para la gráfica
        labels = [item['reclamacion__descripcion'] for item in qs_grouped]
        series = [item['total'] for item in qs_grouped]
        # Top 3 para el footer
        top3 = qs_grouped[:3]
        return {
            'labels': labels,
            'series': series,
            'top3': top3,
        }
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        registro_id = self.request.GET.get('registro')
        registros = Registro.objects.all().order_by('-title')
        qs = self.get_queryset()
        counts = self.get_counts_by_status(qs)
        reclamaciones_data = self.get_reclamaciones_data(qs)
        context.update({
            'counts': counts,
            'graf_quejas_mes' : self.get_graf_quejas_mes(qs),
            'reclamaciones_labels': reclamaciones_data['labels'],
            'reclamaciones_series': reclamaciones_data['series'],
            'reclamaciones_top3': reclamaciones_data['top3'],
            'registros': registros,
            'selected_registro': registro_id,
            'panel': 'Panel de administrador',
            'home': reverse_lazy('gestion:dashboard'),
            'name': 'Panel de Control'
        })
        # Contadores de expedientes por estado
        context['exp_investigacion'] = Expediente.objects.filter(estado_expediente__estado='Investigación').count()
        context['exp_corregir'] = Expediente.objects.filter(estado_expediente__estado='Corregir').count()

        # Permisos de usuario
        user = self.request.user
        context['is_director'] = user.groups.filter(name='Director').exists()
        context['is_tecnico'] = user.groups.filter(name='Tecnicos').exists()
        context['is_admin'] = user.is_superuser or user.is_staff
        
        return context
    
   