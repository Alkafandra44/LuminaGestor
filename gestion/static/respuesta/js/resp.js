$(document).ready(function() {
    $('#tblRespuestasClientes').DataTable({
        responsive: true,
        paging: false,
        searching: false,
        info: false,
        ordering: false,
        language: {
            emptyTable: "No hay datos disponibles"
        }
    });
});

   $(document).ready(function() {
         // Evento para nueva respuesta
         $('.btnNuevaRespuesta').on('click', function(e) {
               e.preventDefault();
               const expedienteId = $(this).data('expediente-id');
               const clienteId = $(this).data('cliente-id');
               const clienteNombre = $(this).data('cliente-nombre');
               
               // Configurar modal para nueva respuesta
               $('#modalRespuestaTitle').text('Nueva Respuesta');
               $('#id_respuesta').val('');
               $('#expediente_id').val(expedienteId);
               $('#cliente_id').val(clienteId);
               $('#id_cliente_nombre').val(clienteNombre);
               $('#destinatario_nombre').val(clienteNombre);
               $('#respuesta').val('');
               $('#evaluacion_gestion').val('');
               $('#resultado_gestion').val('');
               $('#fecha_respuesta').val(new Date().toISOString().split('T')[0]);
               
               $('#modalRespuesta').modal('show');
         });
         
         // Evento para editar respuesta
         $('.btnEditarRespuesta').on('click', function(e) {
               e.preventDefault();
               const respuestaId = $(this).data('respuesta-id');
               
               if (!respuestaId) {
                  alert('No existe respuesta para editar');
                  return;
               }
               
               // Obtener datos de la respuesta
               $.ajax({
                  url: '/gestion/respuesta/get/' + respuestaId + '/',
                  type: 'GET',
                  success: function(response) {
                     if (response.success) {
                           // Configurar modal para editar
                           $('#modalRespuestaTitle').text('Editar Respuesta');
                           $('#id_respuesta').val(response.data.id);
                           $('#expediente_id').val(response.data.expediente_id);
                           $('#cliente_id').val(response.data.cliente_id);
                           $('#destinatario_nombre').val(response.data.cliente_nombre);
                           $('#respuesta').val(response.data.respuesta);
                           $('#evaluacion_gestion').val(response.data.evaluacion_gestion);
                           $('#resultado_gestion').val(response.data.resultado_gestion);
                           $('#fecha_respuesta').val(response.data.fecha_respuesta);
                           
                           $('#modalRespuesta').modal('show');
                     } else {
                           alert('Error al cargar la respuesta: ' + response.error);
                     }
                  }
               });
         });
         
         // Evento para imprimir
         $('.btnImprimirRespuesta').on('click', function(e) {
               e.preventDefault();
               const respuestaId = $(this).data('respuesta-id');
               
               if (!respuestaId) {
                  alert('No existe respuesta para imprimir');
                  return;
               }
               
               // Configurar botón de impresión
               $('#btnImprimirPDF').attr('href', '/gestion/respuesta/print/' + respuestaId + '/');
               $('#modalImprimir').modal('show');
         });
         
         // Enviar formulario de respuesta
         $('#formRespuesta').on('submit', function(e) {
               e.preventDefault();
               const formData = $(this).serialize();
               
               $.ajax({
                  url: '/gestion/respuesta/save/',
                  type: 'POST',
                  data: formData,
                  success: function(response) {
                     if (response.success) {
                           $('#modalRespuesta').modal('hide');
                           location.reload(); // Recargar para ver cambios
                     } else {
                           alert('Error: ' + response.error);
                     }
                  },
                  error: function() {
                     alert('Error al guardar la respuesta');
                  }
               });
         });
      });
      


// var tblRespuestasClientes;
// var modal_title;

// function getData(){
//     if ($.fn.DataTable.isDataTable('#tblRespuestasClientes')) {
//         tblRespuestasClientes.destroy();
//     }

//     tblRespuestasClientes = $('#tblRespuestasClientes').DataTable({
//         responsive: true,
//         autoWidth: false,
//         destroy: true,
//         deferRender: true,
//         ajax:{
//             url: window.location.pathname,
//             type: 'POST',
//             data: {
//                 'action': 'search_respuestas',
//                 'expediente_id': expedienteId 
//             },
//             dataSrc: ""
//         },
//         columns:[
//             {"data": "id"},
//             {
//                 "data": "cliente", 
//                 "render": function(data, type, row) {
//                     return `${data.nombre} ${data.apellido}`;
//                 }
//             },
//             {"data": "evaluacion_gestion"},
//             {"data": "resultado_gestion"},
//             {
//                 "data": "estado",
//                 "render": function(data, type, row) {
//                     return data ? 
//                     '<span class="badge bg-warning">Pendiente</span>' : 
//                     '<span class="badge bg-success">Completada</span>';
//                 }
//             },
//             {"data": "fecha_creacion"},
//         ],
//         columnDefs: [
//             {
//                 targets: [0],
//                 class:'text-center',
//                 orderable: false,
//                 render: function(data, type, row){
//                     var button = '<a href="#" rel="add" class=""btn btn-sm btn-info btn-xs btnNuevaRespuesta btnAdd"><i class="fas fa-plus"></i></a>';
//                     button += '<a href="#" rel="edit" class="btn btn-sm btn-primary btn-xs btnEdit"><i class="fas fa-edit"></i></a>';
//                     button += '<a href="#" rel="print" class=btn btn-success btn-sm btnPrint"><i class="fas fa-print" style="color: white;"></i></a>';
//                     return button;
//                 }
//             },
//         ],
//         initComplete: function(settings, json){
    
//         }  
//     });
// }

// // Función de validación general
// function validateForm() {
//     let isValid = true;
//     const nombre = $('input[name="nombre"]').val();
//     const apellido = $('input[name="apellido"]').val();
//     const carnet = $('input[name="carnet"]').val();
//     const telefono = $('input[name="telefono"]').val();
//     const direccion = $('textarea[name="direccion"]').val();

//     // Validar nombre (letras, empezar con mayúscula)
//     if (!/^[A-ZÁÉÍÓÚÑ][a-záéíóúñ\s]*$/.test(nombre)) {
//         alert('El nombre debe comenzar con mayúscula y contener solo letras');
//         isValid = false;
//     }

//     // Validar apellido (letras, empezar con mayúscula)
//     if (!/^[A-ZÁÉÍÓÚÑ][a-záéíóúñ\s]*$/.test(apellido)) {
//         alert('El apellido debe comenzar con mayúscula y contener solo letras');
//         isValid = false;
//     }

//     // Validar carnet (11 dígitos)
//     if (!/^[0-9]{11}$/.test(carnet)) {
//         alert('El carnet debe tener 11 dígitos numéricos');
//         isValid = false;
//     }

//     // Validar teléfono (8 dígitos, opcional +53 al inicio)
//     if (!/^(\+53)?[0-9]{8}$/.test(telefono)) {
//         alert('Teléfono inválido. Ejemplo válido: +5351234567 o 51234567');
//         isValid = false;
//     }

//     // Validar dirección (letras, números y caracteres permitidos)
//     if (!/^[A-Za-z0-9áéíóúñÁÉÍÓÚÑ\s.,/#]+$/.test(direccion)) {
//         alert('La dirección solo puede contener letras, números y los caracteres ., / #');
//         isValid = false;
//     }

//     return isValid;
// }

// $(function(){

//     modal_title = $('.modal-title');

//     initRespuestasTable();

//     //Add
//     $('.btnNuevoCliente').on('click', function(){
//         $('input[name="action"]').val('add')
//         modal_title.find('span').html(' Crear Nuevo Cliente');
//         modal_title.find('i').removeClass().addClass('fas fa-plus');
//         $('form')[0].reset();
//         $('#myModalCliente').modal('show');
//     });
    
//     $('#tblClientes')
//         //Edit
//         .on('click', 'a[rel="edit"]', function () {
//             modal_title.find('span').html(' Editar Cliente');
//             modal_title.find('i').removeClass().addClass('fas fa-edit');
//             var tr = tblClientes.cell($(this).parent('td, li')).index();
//             var data = tblClientes.row(tr.row).data();
//             $('input[name="action"]').val('edit');
//             $('input[name="id"]').val(data.id_cliente);
//             $('input[name="carnet"]').val(data.carnet);
//             $('input[name="nombre"]').val(data.nombre);
//             $('input[name="apellido"]').val(data.apellido);
//             $('input[name="telefono"]').val(data.telefono);
//             $('textarea[name="direccion"]').val(data.direccion);
//             $('select[name="municipio"]').val(data.municipio_id);
//             $('#myModalCliente').modal('show');
//         })
//         //Delete
//         .on('click', 'a[rel="delete"]', function () {
//             var tr = tblClientes.cell($(this).parent('td, li')).index();
//             var data = tblClientes.row(tr.row).data();
//             var parameters = {
//                 action: 'delete',
//                 id: data.id_cliente
//             };
//             submit_with_ajax(window.location.pathname, 
//                 'Notificacion', 
//                 '¿Estas seguro de eliminar el siguiente registro?', 
//                 parameters, 
//                 function(){
//                     tblClientes.ajax.reload();
//                 }
//             );
//         });

    // $('form').on('submit', function(e) {
    //     e.preventDefault();

    //     if (!validateForm()) {
    //         return false;
    //     }
        
    //     var parameters = $(this).serialize();
    //     submit_with_ajax(window.location.pathname, 'Notificacion', '¿Estas seguro de realizar la siguiente acción?', parameters, function(){
    //         $('#myModalCliente').modal('hide');
    //         tblClientes.ajax.reload();
    //     });
    // });
// });