var tblRespuestasClientes;

function getData(){
    tblRespuestasClientes = $('#tblRespuestasClientes').DataTable({
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
        ],
        columnDefs: [
            {
                targets: [0],
                class:'text-center',
                orderable: false,
                render: function(data, type, row){
                    var button = '<a href="expediente/show/' + row.id_expediente + '/" rel="show" class="btn btn-sm btn-info btn-xs"><i class="fas fa-eye" style="color: white;"></i></a> ';
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