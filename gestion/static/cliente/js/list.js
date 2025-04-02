var tblClientes;

function getData(){
    tblClientes = $('#tblClientes').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax:{
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns:[
            {"data": ""},
            {"data": "carnet"},
            {
                "data": "nombre", 
                "render": function(data, type, row) {
                    return row.nombre + ' ' + row.apellido;
                }
            },
            {"data": "telefono"},
            {
                "data": "direccion", 
                "render": function(data, type, row) {
                    return row.direccion + ', ' + row.municipio;
                }
            },
        ],
        columnDefs: [
            {
                targets: [0],
                class:'text-center',
                orderable: false,
                render: function(data, type, row){
                    var button = '<a href="#" rel="edit" class="btn btn-sm btn-primary btn-xs btnEdit"><i class="fas fa-edit"></i></a>';
                    button += '<a href="#" rel="delete" class="btn btn-sm btn-danger btn-xs btnDelete"><i class="fas fa-trash-alt"></i></a>'
                    return button;
                }
            },
        ],
        initComplete: function(settings, json){
    
        }  
    });
}

$(function(){

    modal_title = $('.modal-title');

    getData();

    //Add
    $('.btnNuevoCliente').on('click', function(){
        $('input[name="action"]').val('add')
        modal_title.find('span').html(' Crear Nuevo Cliente');
        modal_title.find('i').removeClass().addClass('fas fa-plus');
        $('form')[0].reset();
        $('#myModalCliente').modal('show');
    });

    
    $('#tblClientes')
        //Edit
        .on('click', 'a[rel="edit"]', function () {
            modal_title.find('span').html(' Editar Cliente');
            modal_title.find('i').removeClass().addClass('fas fa-edit');
            var tr = tblClientes.cell($(this).parent('td, li')).index();
            var data = tblClientes.row(tr.row).data();
            $('input[name="action"]').val('edit');
            $('input[name="id"]').val(data.id_cliente);
            $('input[name="carnet"]').val(data.carnet);
            $('input[name="nombre"]').val(data.nombre);
            $('input[name="apellido"]').val(data.apellido);
            $('input[name="telefono"]').val(data.telefono);
            $('textarea[name="direccion"]').val(data.direccion);
            $('select[name="municipio"]').val(data.municipio.nombre);
            $('#myModalCliente').modal('show');
        })
        //Delete
        .on('click', 'a[rel="delete"]', function () {
            var tr = tblClientes.cell($(this).parent('td, li')).index();
            var data = tblClientes.row(tr.row).data();
            var parameters = {
                action: 'delete',
                id: data.id_cliente
            };
            submit_with_ajax(window.location.pathname, 'Notificacion', '¿Estas seguro de eliminar el siguiente registro?', parameters, function(){
                tblClientes.ajax.reload();
            });
        });

    $('form').on('submit', function(e) {
        e.preventDefault();
        var parameters = new FormData(this);
        submit_with_ajax(window.location.pathname, 'Notificacion', '¿Estas seguro de realizar la siguiente acción?', parameters, function(){
            $('#myModalCliente').modal('hide');
            
            tblClientes.ajax.reload();
        });
    });
});