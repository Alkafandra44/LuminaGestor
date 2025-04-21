var tblExpedientes;
var modal_title;

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
            {"data": "fecha_create"},
            {"data": "fecha_complete"},
            {"data": "estado_expediente"},
        ],
        columnDefs: [
            {
                targets: [0],
                class:'text-center',
                orderable: false,
                render: function(data, type, row){
                    var button = '<a href="detalle/' + row.id_expediente + '/" rel="show" class="btn btn-sm btn-info btn-xs"><i class="fas fa-eye" style="color: white;"></i></a> ';
                    button += '<a href="#" rel="edit" class="btn btn-sm btn-primary btn-xs btnEdit"><i class="fas fa-edit"></i></a> ';
                    button += '<a href="#" rel="delete" class="btn btn-sm btn-danger btn-xs"><i class="fas fa-trash-alt"></i></a> '
                    return button;
                }
            },
            {
                targets: [1, 2, 3, 4, 5, 6], 
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
    $('.btnNuevoExpediente').on('click', function(){
        $('input[name="action"]').val('add')
        modal_title.find('span').html(' Crear Nuevo Expediente');
        modal_title.find('i').removeClass().addClass('fas fa-plus');
        $('form')[0].reset();
        $('#myModalExpediente').modal('show');
    });
});