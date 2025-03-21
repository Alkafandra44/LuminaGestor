function alert_error(obj){
    var html = '<p>';
    $.each(obj, function (key, value) { //por ahora no me hace falta el key
        html += '<h5>' + value + '</h5>';
    });
    html +='</p>';
    Swal.fire({
        title: "Error!",
        html: html,
        icon: "error",
      });
}