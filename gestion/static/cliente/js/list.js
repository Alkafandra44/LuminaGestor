$(function(){
    $('#tblClientes').DataTable({
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
                "data": null, 
                "render": function(data, type, row) {
                    return row.nombre + ' ' + row.apellido;
                }
            },
            {"data": "telefono"},
            {
                "data": null, 
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
                    var button = '<a href="/gestion/clientes/edit/' + row.id_cliente + '/" class="btn btn-sm btn-primary btn-xs"><i class="fas fa-edit"></i></a>';
                    button += '<a href="/gestion/clientes/delete/'  + row.id_cliente + '/" class="btn btn-sm btn-danger btn-xs"><i class="fas fa-trash-alt"></i></a>'
                    return button;
                }
            },
        ],
        initComplete: function(settings, json){
    
        }  
    });
});