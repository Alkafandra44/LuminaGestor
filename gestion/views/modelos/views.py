from datetime import datetime
import locale
import os
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from gestion.models import RespuestaCliente

# ===========PARA XHTML2PDF
import os
from django.conf import settings
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


## Para la impresion de Respuestas y Modelos (Mover a otro view)
class ExpedienteInvoivePdfView(View):
    
    def link_callback(self, uri, rel):
        # Usa el sistema de finders de Django
        if uri.startswith(('http://', 'https://')):
            return uri  # Maneja URLs externas si es necesario
        
        # Busca en STATICFILES_DIRS y STATIC_ROOT
        path = finders.find(uri)
        
        if not path:
            # Intenta construir la ruta manualmente
            if uri.startswith(settings.STATIC_URL):
                rel_path = uri.replace(settings.STATIC_URL, "", 1)
                for static_dir in settings.STATICFILES_DIRS:
                    candidate = os.path.join(static_dir, rel_path)
                    if os.path.exists(candidate):
                        path = candidate
                        break
        
        if not path or not os.path.exists(path):
            # Log de error para depuración
            print(f"Archivo no encontrado: {uri}")
            return uri
        
        return path

    def get(self, request, respuesta_id, *args, **kwargs):
        respuesta = RespuestaCliente.objects.select_related('expediente', 'cliente').get(pk=respuesta_id)
        template = get_template('modelos/invoice_pdf.html')
        now = datetime.now()
        try:
            template = get_template('modelos/invoice_pdf.html')
            
                # Fecha actual
            now = datetime.now()
            dia = now.day
            # Para mes en español:
            try: 
                locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # O 'es_ES' según tu sistema
                mes = now.strftime('%B').capitalize()
            except:
                # Fallback si no está disponible el locale
                meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
                        'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
                mes = meses[now.month - 1].capitalize()
            anio = now.year
            anio_rev = anio - 1958
            
            context = {
                'title': 'UEB CIAC',
                'logo': 'img/logo_resp.jpg',
                'header': 'img/header_resp.jpg',
                'dia': dia,
                'mes': mes,
                'anio': anio,
                'anio_rev': anio_rev,
                'respuesta': respuesta,
                'expediente': respuesta.expediente, 
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="respuesta.pdf"'

            pisa_status = pisa.CreatePDF(
                html,
                dest=response,
                link_callback=self.link_callback,
            )
            if pisa_status.err:
                return HttpResponse('Hemos tenido un problema <pre>' + html + '</pre>')
            return response
        except Exception as e:
            # Muestra el error en pantalla para depuración
            return HttpResponse(f'Error al generar PDF: {e}')


@method_decorator(csrf_exempt, name='dispatch')
class ResumenPDFView(LoginRequiredMixin, View):
    
    def link_callback(self, uri, rel):
        # Usa el sistema de finders de Django
        if uri.startswith(('http://', 'https://')):
            return uri  # Maneja URLs externas si es necesario
        
        # Busca en STATICFILES_DIRS y STATIC_ROOT
        path = finders.find(uri)
        
        if not path:
            # Intenta construir la ruta manualmente
            if uri.startswith(settings.STATIC_URL):
                rel_path = uri.replace(settings.STATIC_URL, "", 1)
                for static_dir in settings.STATICFILES_DIRS:
                    candidate = os.path.join(static_dir, rel_path)
                    if os.path.exists(candidate):
                        path = candidate
                        break
        
        if not path or not os.path.exists(path):
            # Log de error para depuración
            print(f"Archivo no encontrado: {uri}")
            return uri
        
        return path
    
    def post(self, request, *args, **kwargs):
        resumen = request.POST.get('resumen', '')
        template = get_template('modelos/resumen_pdf.html')
        
        # Fecha actual
        now = datetime.now()
        dia = now.day
        # Para mes en español:
        try: 
            locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # O 'es_ES' según tu sistema
            mes = now.strftime('%B').capitalize()
        except:
            # Fallback si no está disponible el locale
            meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
                     'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
            mes = meses[now.month - 1].capitalize()
        anio = now.year
        anio_rev = anio - 1958
        
        html = template.render({
            'resumen': resumen, 
            'user': request.user,
            'rol': request.user.groups.first().name if request.user.groups.exists() else 'Usuario',
            'logo': 'img/logo_resp.jpg',
            'header': 'img/header_resp.jpg',
            'title': 'Resumen del Expediente',
            'dia': dia,
            'mes': mes,
            'anio': anio,
            'anio_rev': anio_rev,
            })
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="resumen.pdf"'
        
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('Error al generar PDF', status=500)
        return response