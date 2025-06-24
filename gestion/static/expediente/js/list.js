var tblExpedientes;

function getData(){
    tblExpedientes = $('#tblExpedientes').DataTable({
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
            {"data": "id_expediente"},
            {"data": "title"},//nombre
            {"data": "clasificacion"},
            {"data": "reclamacion"},
            {"data": "estado_expediente"},
            {"data": "fecha_create"},
            {"data": "fecha_entrega"},
            {"data": "user.username"},
        ],
        columnDefs: [
            {
                targets: [0],
                class:'text-center',
                orderable: false,
                render: function(data, type, row){
                    var button = '<a href="expediente/show/' +  row.id_expediente + '/" rel="show" class="btn btn-sm btn-info btn-xs"><i class="fas fa-eye" style="color: white;"></i></a> ';
                    if (userHasEditPermission && row.estado_expediente !== 'Solucionado') {
                        button += '<a href="expediente/update/' +  row.id_expediente + '/" rel="edit" class="btn btn-sm btn-primary btn-xs btnEdit"><i class="fas fa-search"></i></a> ';
                    }
                    return button;
                }
            },
            {
                targets: [5], // Columna de grupos
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    //Personalizacion del color segun el estado
                    var badgeClass = 'text-bg-secondary';
                    if(data === 'Pendiente') badgeClass = 'text-bg-warning';
                    else if(data === 'Investigación') badgeClass = 'text-bg-info';
                    else if(data === 'Solucionado') badgeClass = 'text-bg-success';
                    else if(data === 'Revisión') badgeClass = 'text-bg-danger';
                    else if(data === 'Corregir') badgeClass = 'text-bg-danger';
                    
                    return '<span class="badge ' + badgeClass + '">' + data + '</span>';
                }
            },
            {
                targets: [1, 2, 3, 4, 5, 6, 7], 
                class: 'text-center', 
            },
        ],
        initComplete: function(settings, json){
            $('#btnNuevoExpediente').on('click', function(e) {
                e.preventDefault();
                window.location.href = $(this).attr('href');
            });
    
        }  
    });
}

// Validación en tiempo real para el título (letras y números)
$(document).on('input', 'input[name="title"]', function() {
    this.value = this.value.replace(/[^A-Za-z0-9ÁÉÍÓÚáéíóúÑñ\s]/g, '');
    if (this.value.length > 0) {
        this.value = this.value.charAt(0).toUpperCase() + this.value.slice(1);
    }
});

// Validación en tiempo real para el resumen (letras, números, espacios y . , / #, primera letra mayúscula)
$(document).on('input', 'textarea[name="resumen"]', function() {
    this.value = this.value.replace(/[^A-Za-z0-9áéíóúñÁÉÍÓÚÑ\s.,/#]/g, '');
    if (this.value.length > 0) {
        this.value = this.value.charAt(0).toUpperCase() + this.value.slice(1);
    }
});

// Validación de archivos al seleccionar
$(document).on('change', 'input[name="archivos"]', function() {
    const files = this.files;
    const validTypes = [
        'application/pdf', 'application/msword', 
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.ms-excel', 
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'image/jpeg', 'image/png'
    ];
    let errorMsg = '';
    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        if (!validTypes.includes(file.type)) {
            errorMsg = "Tipo de archivo no permitido: " + file.name;
            break;
        } else if (file.size > 5 * 1024 * 1024) {
            errorMsg = "El archivo " + file.name + " es demasiado grande (máx 5MB) y no se guardará";
            break;
        }
    }
    if (errorMsg) {
        showError($(this), errorMsg);
        Swal.fire({
            icon: 'error',
            title: 'Error de archivo',
            text: errorMsg
        });
        this.value = ''; // Limpia el input
    } else {
        clearError($(this));
    }
});

function validateExpedienteFormSwal() {
    let errors = [];
    const title = $('input[name="title"]').val();
    const resumen = $('textarea[name="resumen"]').val();
    const archivos = $('input[name="archivos"]')[0].files;

    // Título: solo letras y números, más de 5 caracteres, empieza con mayúscula
    if (!/^[A-ZÁÉÍÓÚÑ]/.test(title)) {
        errors.push('El título debe comenzar con letra mayúscula.');
    }
    if (!/^[A-Za-z0-9ÁÉÍÓÚáéíóúÑñ\s]+$/.test(title) || title.length <= 5) {
        errors.push('El título debe tener más de 5 caracteres y solo puede contener letras y números.');
    }

    // Resumen: solo letras, números y . , / #, más de 50 caracteres, empieza con mayúscula
    if (resumen.length > 0) {
        if (!/^[A-ZÁÉÍÓÚÑ]/.test(resumen)) {
            errors.push('El resumen debe comenzar con letra mayúscula.');
        }
        if (!/^[A-Za-z0-9áéíóúñÁÉÍÓÚÑ\s.,/#]+$/.test(resumen) || resumen.length <= 50) {
            errors.push('El resumen debe tener más de 50 caracteres y solo puede contener letras, números y los caracteres ., / #');
        }
    }
    const validTypes = [
        'application/pdf', 'application/msword', 
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.ms-excel', 
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'image/jpeg', 'image/png'
    ];
    for (let i = 0; i < archivos.length; i++) {
        const file = archivos[i];
        if (!validTypes.includes(file.type)) {
            errors.push("Tipo de archivo no permitido: " + file.name);
            break;
        } else if (file.size > 5 * 1024 * 1024) {
            errors.push("El archivo " + file.name + " es demasiado grande (máx 5MB)");
            break;
        }
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

function showError(element, message) {
    element.addClass('is-invalid');
    element.next('.invalid-feedback').remove();
    element.after(`<div class="invalid-feedback">${message}</div>`);
}

function clearError(element) {
    element.removeClass('is-invalid');
    element.next('.invalid-feedback').remove();
}

$(function(){
    modal_title = $('.modal-title');

    getData();

    // Evento para el botón de editar expediente
    $('#tblExpedientes').on('click', 'a[rel="edit"]', function(e) {
        e.preventDefault();
        window.location.href = $(this).attr('href');
    });
    // Evento para el botón de ver expediente
    $('#tblExpedientes').on('click', 'a[rel="show"]', function(e) {
        e.preventDefault();
        $('.form-page').show();
        window.location.href = $(this).attr('href');
    });

    // Validación al submit del formulario
    $('#formulariocl').on('submit', function(e) {
        if (!validateExpedienteFormSwal()) {
            e.preventDefault();
            return false;
        }
    });
});