var tblRegistros;
var modal_title;

function getData(){
    tblRegistros = $('#tblRegistros').DataTable({
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
            {"data": "title"},
            {"data": "fecha_creacion"},
        ],
        columnDefs: [
            {
                targets: [0],
                class:'text-center',
                orderable: false,
                render: function(data, type, row){
                    var button = '<a href="detalle/' + row.id_registro + '/" rel="show" class="btn btn-sm btn-info btn-xs"><i class="fas fa-eye" style="color: white;"></i></a> ';
                    if(userHasEditPermission){
                        button += '<a href="#" rel="edit" class="btn btn-sm btn-primary btn-xs btnEdit"><i class="fas fa-edit"></i></a> ';
                    }
                    if(userHasDeletePermission){
                        button += '<a href="#" rel="delete" class="btn btn-sm btn-danger btn-xs"><i class="fas fa-trash-alt"></i></a> ';
                    }
                    return button;
                }
            },
            {
                targets: [1, 2], 
                class: 'text-center', 
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
    $('.btnNuevoRegistro').on('click', function(){
        $('input[name="action"]').val('add')
        modal_title.find('span').html(' Crear Nuevo Registro');
        modal_title.find('i').removeClass().addClass('fas fa-plus');
        $('form')[0].reset();
        $('#myModalRegistro').modal('show');
    });
    
    $('#tblRegistros tbody')
 
        //Edit
        .on('click', 'a[rel="edit"]', function () {   
            modal_title.find('span').html(' Editar Registro');
            modal_title.find('i').removeClass().addClass('fas fa-edit');
            var tr = tblRegistros.cell($(this).closest('td, li')).index();
            var data = tblRegistros.row(tr.row).data();
            $('input[name="action"]').val('edit');
            $('input[name="id"]').val(data.id_registro);
            $('input[name="title"]').val(data.title);
            $('#myModalRegistro').modal('show');
        })
        //Delete
        .on('click', 'a[rel="delete"]', function () {  
            modal_title.find('span').html(' Editar Registro');
            modal_title.find('i').removeClass().addClass('fas fa-edit');
            var tr = tblRegistros.cell($(this).closest('td, li')).index();
            var data = tblRegistros.row(tr.row).data();
            var parameters = {
                action: 'delete',
                id: data.id_registro
            };
            submit_with_ajax(window.location.pathname, 'Notificacion', '¿Estas seguro de eliminar el siguiente registro?', parameters, function(){
                tblRegistros.ajax.reload();
            });
        });

    $('form').on('submit', function(e) {
        e.preventDefault();
        var parameters = $(this).serialize();
            $.ajax({
            url: window.location.pathname,
            type: "POST",
            data: parameters,
            dataType: "json",
        }).done(function (data) {
            if (!data.hasOwnProperty("error")) {
                $('#myModalRegistro').modal('hide');
                tblRegistros.ajax.reload();
                Swal.fire({
                    icon: 'success',
                    title: '¡Registro guardado!',
                    showConfirmButton: false,
                    timer: 1500
                });
                return false;
            }
            // Manejo de errores con SweetAlert
            var html = '';
            try {
                var errors = JSON.parse(data.error);
                html = "<ul>";
                $.each(errors, function (key, value) {
                    value.forEach(function(err){
                        html += "<li><b>" + key + ":</b> " + err.message + "</li>";
                    });
                });
                html += "</ul>";
            } catch (e) {
                html = "<p>" + data.error + "</p>";
            }
            Swal.fire({
                title: "Error de validación",
                html: html,
                icon: "error",
            });
        }).fail(function (jqXHR, textStatus, errorThrown) {
            Swal.fire({
                title: "Error",
                text: textStatus + ": " + errorThrown,
                icon: "error",
            });
        tblRegistros.ajax.reload();
        });
    });
});