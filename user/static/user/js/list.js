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
            {"data": "id"},
            {"data": "first_name"},
            {"data": "last_name"},
            {"data": "username"},
            {"data": "email"},
            {"data": "groups"},
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
                targets: [5], // Columna de grupos
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var html = '';
                    $.each(data, function (key, value) {
                        html += '<span class="badge text-bg-success">' + value + '</span> ';
                    });
                    return html;
                }
            },
            {
                targets: [0],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '';
                    if(row.is_superuser == true){
                        return '<span class="badge text-bg-info">ADMIN</span>';
                    }
                    if(userHasEditPermission){
                        buttons = '<a href="#" rel="edit" class="btn btn-sm btn-primary btn-xs btnEdit"><i class="fas fa-edit"></i></a>';
                    }
                    if(userHasDeletePermission){
                        buttons += '<a href="#" rel="delete" class="btn btn-sm btn-danger btn-xs"><i class="fas fa-trash-alt"></i></a> ';
                    }
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

// Nombre: solo letras, mínimo 2, primera mayúscula
$(document).on('input', 'input[name="first_name"]', function() {
    this.value = this.value.replace(/[^A-Za-zÁÉÍÓÚáéíóúÑñ\s]/g, '');
    if (this.value.length > 0) {
        this.value = this.value.charAt(0).toUpperCase() + this.value.slice(1);
    }
});

// Apellidos: solo letras, mínimo 2, primera mayúscula
$(document).on('input', 'input[name="last_name"]', function() {
    this.value = this.value.replace(/[^A-Za-zÁÉÍÓÚáéíóúÑñ\s]/g, '');
    if (this.value.length > 0) {
        this.value = this.value.charAt(0).toUpperCase() + this.value.slice(1);
    }
});

// Nombre de usuario: letras y números, mínimo 2
$(document).on('input', 'input[name="username"]', function() {
    this.value = this.value.replace(/[^A-Za-z0-9]/g, '');
});

// Contraseña: letras y números, mínimo 8, cambia color del borde
$(document).on('input', 'input[name="password"]', function() {
    this.value = this.value.replace(/[^A-Za-z0-9]/g, '');
    let $input = $(this);
    if (this.value.length < 8) {
        $input.css('border', '2px solid red');
    } else if (this.value.length < 12) {
        $input.css('border', '2px solid orange');
    } else {
        $input.css('border', '2px solid green');
    }
});

// Cambiar label de grupo a "Rol"
$(function() {
    $('label[for="id_groups"]').text('Rol:');
});

// Validación al enviar el formulario
function validateUserFormSwal() {
    let errors = [];
    const nombre = $('input[name="first_name"]').val();
    const apellido = $('input[name="last_name"]').val();
    const username = $('input[name="username"]').val();
    const email = $('input[name="email"]').val();
    const password = $('input[name="password"]').val();
    const grupo = $('select[name="groups"]').val();

    // Nombre
    if (!/^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]{2,}$/.test(nombre)) {
        errors.push('El nombre debe tener al menos 2 letras y solo letras.');
    }
    // Apellido
    if (!/^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]{2,}$/.test(apellido)) {
        errors.push('El apellido debe tener al menos 2 letras y solo letras.');
    }
    // Usuario
    if (!/^[A-Za-z0-9]{2,}$/.test(username)) {
        errors.push('El nombre de usuario debe tener al menos 2 caracteres y solo letras o números.');
    }
    // Correo
    if (!/^[^@]+@[^@]+\.[^@]+$/.test(email)) {
        errors.push('Debe ingresar un correo electrónico válido.');
    }
    // Contraseña
    if (!/^[A-Za-z0-9]{8,}$/.test(password)) {
        errors.push('La contraseña debe tener al menos 8 caracteres y solo letras o números.');
    }
    // Grupo
    if (!grupo) {
        errors.push('Debe seleccionar un rol.');
    }

    if (errors.length > 0) {
        Swal.fire({
            icon: 'error',
            title: 'Errores de validación',
            html: '<ul style="text-align:left;">' + errors.map(e => `<li>${e}</li>`).join('') + '</ul>'
        });
        return false;
    }
    return true;
}

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
            $('input[name="last_name"]').val(data.last_name);
            $('input[name="username"]').val(data.username);
            $('input[name="email"]').val(data.email);
            $('select[name="groups"]').val(data.groups_id);
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
        if (!validateUserFormSwal()) {
            return false;
        }
        var parameters = $(this).serialize();
        submit_with_ajax(window.location.pathname, 'Notificacion', '¿Estas seguro de realizar la siguiente acción?', parameters, function(){
            $('#myModalUser').modal('hide');
            tblUser.ajax.reload();
        });
    });


});