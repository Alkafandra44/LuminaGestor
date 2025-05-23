from django.views.generic import TemplateView
from django.urls import reverse_lazy
from datetime import datetime
from django.db.models import Count, Case, When, IntegerField

from gestion.models import Expediente

class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'
    
    # Método para contar expedientes por estado
    def get_counts_by_status(self):
        # Una sola consulta para todos los contadores
        return Expediente.objects.aggregate(
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
            )
        )
    
    # Método para gráfica de barras
    def get_graf_quejas_mes(self):
        year = datetime.now().year
        expediente_por_mes = []
        for mes in range(1, 13):
            count = Expediente.objects.filter(
                fecha_create__year=year, 
                fecha_create__month=mes
            ).count()
            expediente_por_mes.append(count)
        return expediente_por_mes
    
    # Método para gráfica de Pastel
    # def get_graf_clasificacion(self):
    #     # Una sola consulta para todos los contadores
    #     return Expediente.objects.aggregate(
    #         total=Count('id_expediente'),
    #         lineasypostes=Count(
    #             Case(
    #                 When(reclamacion__reclamacion='Lineas y Postes', then=1),
    #                 output_field=IntegerField()
    #             )
    #         ),
    #         investigacion=Count(
    #             Case(
    #                 When(estado_expediente__estado='Investigación', then=1),
    #                 output_field=IntegerField()
    #             )
    #         ),
    #         solucionados=Count(
    #             Case(
    #                 When(estado_expediente__estado='Solucionado', then=1),
    #                 output_field=IntegerField()
    #             )
    #         )
    #     )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        counts = self.get_counts_by_status() 
        context.update({
            'counts': counts,
            'graf_quejas_mes' : self.get_graf_quejas_mes(),
            'panel': 'Panel de administrador',
            'home': reverse_lazy('gestion:dashboard'),
            'name': 'Panel de Control'
        })
        return context
    
   