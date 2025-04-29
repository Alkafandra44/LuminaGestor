var tblUser;

function getData() {
    tblUser = $('#tblUser').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": ""},
            {"data": "first_name"},
            {"data": "username"},
            {"data": "email"},
            {"data": "rol"},
            {"data": "date_joined"},
        ],
        columnDefs: [
            /*{
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var html = '';
                    $.each(row.groups, function (key, value) {
                        html += '<span class="badge badge-success">' + value.name + '</span> ';
                    });
                    return html;
                }
            },*/
            {
                targets: [0],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" rel="edit" class="btn btn-sm btn-primary btn-xs btnEdit"><i class="fas fa-edit"></i></a>';
                    buttons += '<a href="#" rel="delete" class="btn btn-sm btn-danger btn-xs"><i class="fas fa-trash-alt"></i></a> ';
                    return buttons;
                }
            },
            {
                targets: [1, 2, 3, 4, 5],
                class: 'text-center',
            },
        ],
        initComplete: function (settings, json) {

        }
    });
};

var modal_title;
$(function(){

    modal_title = $('.modal-title'); 

    getData();

    //Add
    $('.btnNuevoUser').on('click', function(){
        $('input[name="action"]').val('add')
        modal_title.find('span').html(' Crear Nuevo Usuario');
        modal_title.find('i').removeClass().addClass('fas fa-plus');
        $('form')[0].reset();
        $('#myModalUser').modal('show');
    });
    //Edit
    $('#tblUser')
        .on('click', 'a[rel="edit"]', function () {
            modal_title.find('span').html(' Editar Usuario');
            modal_title.find('i').removeClass().addClass('fas fa-edit');
            var tr = tblUser.cell($(this).closest('td, li')).index();
            var data = tblUser.row(tr.row).data();
            $('input[name="action"]').val('edit');
            $('input[name="id"]').val(data.id);
            $('input[name="first_name"]').val(data.first_name);
            $('input[name="username"]').val(data.username);
            $('input[name="email"]').val(data.email);
            $('select[name="rol"]').val(data.rol).trigger('change');
            //$('input[name="password"]').val(data.password);
            $('#myModalUser').modal('show');
        })
        //Delete
        .on('click', 'a[rel="delete"]', function () {
            var tr = tblUser.cell($(this).closest('td, li')).index();
            var data = tblUser.row(tr.row).data();
            var parameters = {
                action: 'delete',
                id: data.id
            };
            submit_with_ajax(window.location.pathname, 'Notificacion', '¿Estas seguro de eliminar el siguiente registro?', parameters, function(){
                tblUser.ajax.reload();
            });
        });


    $('form').on('submit', function(e) {
        e.preventDefault();
        var parameters = $(this).serialize();
        submit_with_ajax(window.location.pathname, 'Notificacion', '¿Estas seguro de realizar la siguiente acción?', parameters, function(){
            $('#myModalUser').modal('hide');
            tblUser.ajax.reload();
        });
    });


});