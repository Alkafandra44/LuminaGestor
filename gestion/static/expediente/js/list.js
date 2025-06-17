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
                    if (userHasEditPermission) {
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


function setupFormValidation() {
    // Validar título
    $('input[name="title"]').on('input', function() {
        const value = $(this).val();
        if (value.length > 0 && !/^[A-ZÁÉÍÓÚÑ]/.test(value)) {
            showError($(this), "Debe comenzar con mayúscula");
        } else {
            clearError($(this));
        }
    });
        
    // Validar archivos
    $('input[name="archivos"]').on('change', function() {
        const file = this.files[0];
        if (file) {
            const validTypes = ['application/pdf', 'application/msword', 
                              'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                              'application/vnd.ms-excel', 
                              'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                              'image/jpeg', 'image/png'];
            
            if (!validTypes.includes(file.type)) {
                showError($(this), "Tipo de archivo no permitido");
            } else if (file.size > 5 * 1024 * 1024) {
                showError($(this), "El archivo es demasiado grande (máx 5MB)");
            } else {
                clearError($(this));
            }
        }
    });
    
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

    // Configurar validación del formulario
    setupFormValidation();

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

});

