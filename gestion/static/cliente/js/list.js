var tblClientes;
var modal_title;

// --- VALIDACIONES EN TIEMPO REAL ---
$(document).on('input', 'input[name="carnet"]', function() {
    // Solo números y máximo 11 dígitos
    this.value = this.value.replace(/\D/g, '').slice(0, 11);
});

$(document).on('blur', 'input[name="carnet"]', function() {
    if (this.value.length !== 11) {
        Swal.fire({
            icon: 'error',
            title: 'Carnet inválido',
            text: 'El carnet debe tener exactamente 11 dígitos.'
        });
    } else {
        // Validar fecha de nacimiento
        let year = this.value.substring(0, 2); // Puede ser '00'
        let month = parseInt(this.value.substring(2, 4), 10);
        let day = parseInt(this.value.substring(4, 6), 10);
        if (month < 1 || month > 12 || day < 1 || day > 31) {
            Swal.fire({
                icon: 'error',
                title: 'Carnet inválido',
                text: 'El carnet no tiene una fecha válida.'
            });
        }
    }
});

$(document).on('input', 'input[name="nombre"]', function() {
    // Solo letras y espacios, mínimo 2 caracteres
    this.value = this.value.replace(/[^A-Za-zÁÉÍÓÚáéíóúÑñ\s]/g, '');
    if (this.value.length > 0) {
        this.value = this.value.charAt(0).toUpperCase() + this.value.slice(1);
    }
});

$(document).on('input', 'input[name="apellido"]', function() {
    // Solo letras y espacios, mínimo 2 caracteres
    this.value = this.value.replace(/[^A-Za-zÁÉÍÓÚáéíóúÑñ\s]/g, '');
    if (this.value.length > 0) {
        this.value = this.value.charAt(0).toUpperCase() + this.value.slice(1);
    }
});

$(document).on('input', 'input[name="telefono"]', function() {
    // Solo números y máximo 8 dígitos
    this.value = this.value.replace(/\D/g, '').slice(0, 8);
});

$(document).on('input', 'textarea[name="direccion"]', function() {
    // Solo letras, números, espacios y . , / #
    this.value = this.value.replace(/[^A-Za-z0-9áéíóúñÁÉÍÓÚÑ\s.,/#]/g, '');
});

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
                    if(userHasDeletePermission){
                        button += '<a href="#" rel="delete" class="btn btn-sm btn-danger btn-xs btnDelete"><i class="fas fa-trash-alt"></i></a>'
                    }
                    return button;
                }
            },
        ],
        initComplete: function(settings, json){
    
        }  
    });
}

// --- VALIDACIÓN AL SUBMIT ---
function validateFormSwal() {
    let errors = [];
    const nombre = $('input[name="nombre"]').val();
    const apellido = $('input[name="apellido"]').val();
    const carnet = $('input[name="carnet"]').val();
    const telefono = $('input[name="telefono"]').val();
    const direccion = $('textarea[name="direccion"]').val();
    const municipio = $('select[name="municipio"]').val();

    // Carnet
    if (!/^\d{11}$/.test(carnet)) {
        errors.push('El carnet debe tener exactamente 11 dígitos.');
    } else {
        let year = carnet.substring(0, 2); // Puede ser '00'
        let month = parseInt(carnet.substring(2, 4), 10);
        let day = parseInt(carnet.substring(4, 6), 10);
        if (month < 1 || month > 12 || day < 1 || day > 31) {
            errors.push('El carnet no tiene una fecha válida.');
        }
    }

    // Nombre
    if (!/^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]{2,}$/.test(nombre)) {
        errors.push('El nombre debe tener al menos 2 letras y solo letras.');
    }

    // Apellido
    if (!/^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]{2,}$/.test(apellido)) {
        errors.push('El apellido debe tener al menos 2 letras y solo letras.');
    }

    // Teléfono
    if (!/^\d{8}$/.test(telefono)) {
        errors.push('El teléfono debe tener exactamente 8 dígitos.');
    }

    // Dirección
    if (!/^[A-Za-z0-9áéíóúñÁÉÍÓÚÑ\s.,/#]+$/.test(direccion) || direccion.length < 2) {
        errors.push('La dirección solo puede contener letras, números y los caracteres ., / # (mínimo 2 caracteres).');
    }

    // Municipio
    if (!municipio) {
        errors.push('Debe seleccionar un municipio.');
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
            $('select[name="municipio"]').val(data.municipio_id);
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
            submit_with_ajax(window.location.pathname, 
                'Notificacion', 
                '¿Estas seguro de eliminar el siguiente registro?', 
                parameters, 
                function(){
                    tblClientes.ajax.reload();
                }
            );
        });

    $('form').on('submit', function(e) {
        e.preventDefault();

        if (!validateFormSwal()) {
            return false;
        }
        
        var parameters = $(this).serialize();
        submit_with_ajax(window.location.pathname, 'Notificacion', '¿Estas seguro de realizar la siguiente acción?', parameters, function(){
            $('#myModalCliente').modal('hide');
            tblClientes.ajax.reload();
        });
    });
});