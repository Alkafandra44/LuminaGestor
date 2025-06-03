// // respuestas.js
// $(function() {
//     var modalRespuesta = $('#myModalRespuesta');
//     var formRespuesta = $('#formularioresp');
//     var modalTitle = $('#modalRespuestaTitle span');
//     var modalIcon = $('#modalRespuestaTitle i');

//     // Botón de agregar respuesta
//     $('.btn-add-respuesta').on('click', function() {
//         var expedienteId = $(this).data('expediente-id');
//         var clienteId = $(this).data('cliente-id');
        
//         formRespuesta.find('#expediente_id').val(expedienteId);
//         formRespuesta.find('#cliente_id').val(clienteId);
//         formRespuesta.find('input[name="action"]').val('add');
//         formRespuesta.find('#id_respuesta').val('0');
//         formRespuesta[0].reset();
        
//         modalTitle.text(' Nueva Respuesta');
//         modalIcon.removeClass().addClass('fas fa-plus');
//         modalRespuesta.modal('show');
//     });

//     // Botón de editar respuesta
//     $('.btn-edit-respuesta').on('click', function() {
//         var respuestaId = $(this).data('respuesta-id');
        
//         $.ajax({
//             url: '{% url "gestion:get_respuesta" %}',
//             type: 'GET',
//             data: {
//                 'id': respuestaId
//             },
//             success: function(data) {
//                 if(data.respuesta) {
//                     formRespuesta.find('#id_respuesta').val(data.respuesta.id);
//                     formRespuesta.find('#expediente_id').val(data.respuesta.expediente_id);
//                     formRespuesta.find('#cliente_id').val(data.respuesta.cliente_id);
//                     formRespuesta.find('textarea[name="respuesta"]').val(data.respuesta.respuesta);
//                     formRespuesta.find('select[name="evaluacion_gestion"]').val(data.respuesta.evaluacion_gestion);
//                     formRespuesta.find('select[name="resultado_gestion"]').val(data.respuesta.resultado_gestion);
//                     formRespuesta.find('input[name="action"]').val('edit');
                    
//                     modalTitle.text(' Editar Respuesta');
//                     modalIcon.removeClass().addClass('fas fa-edit');
//                     modalRespuesta.modal('show');
//                 }
//             },
//             error: function() {
//                 Swal.fire('Error', 'No se pudo cargar la respuesta', 'error');
//             }
//         });
//     });

//     // Enviar formulario de respuesta
//     formRespuesta.on('submit', function(e) {
//         e.preventDefault();
//         var formData = new FormData(this);
        
//         $.ajax({
//             url: $(this).attr('action'),
//             type: 'POST',
//             data: formData,
//             processData: false,
//             contentType: false,
//             success: function(data) {
//                 if(data.success) {
//                     modalRespuesta.modal('hide');
//                     Swal.fire('Éxito', data.message, 'success').then(() => {
//                         location.reload();
//                     });
//                 } else {
//                     Swal.fire('Error', data.error, 'error');
//                 }
//             },
//             error: function() {
//                 Swal.fire('Error', 'Error en el servidor', 'error');
//             }
//         });
//     });
    
//     // Botón de imprimir
//     $('.btn-print-respuesta').on('click', function() {
//         var respuestaId = $(this).data('respuesta-id');
//         if(respuestaId) {
//             window.open('{% url "gestion:respuesta_pdf" 0 %}'.replace('0', respuestaId), '_blank');
//         } else {
//             Swal.fire('Advertencia', 'Primero debe crear una respuesta', 'warning');
//         }
//     });
// });