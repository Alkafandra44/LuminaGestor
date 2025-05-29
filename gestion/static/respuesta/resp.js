// $(function(){

//     modal_title = $('.modal-title');

//     getData();

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

//     $('form').on('submit', function(e) {
//         e.preventDefault();

//         if (!validateForm()) {
//             return false;
//         }
        
//         var parameters = $(this).serialize();
//         submit_with_ajax(window.location.pathname, 'Notificacion', '¿Estas seguro de realizar la siguiente acción?', parameters, function(){
//             $('#myModalCliente').modal('hide');
//             tblClientes.ajax.reload();
//         });
//     });
// });