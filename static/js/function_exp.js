function alert_error(obj) {
  var html = '';
  if (typeof obj === "object") {
    html = "<p>";
    $.each(obj, function (key, value) {
      html += "<h5>" + value + "</h5>";
    });
    html += "</p>";
  }
  else{
    html = "<p>" + obj + "</p>";
  }
  Swal.fire({
    title: "Error!",
    html: html,
    icon: "error",
  });
}

function submit_with_ajax(url, title, content, parameters, callback) {
  $.confirm({
    theme: "material",
    title: title,
    icon: "fa fa-info",
    content: content,
    columnClass: "medium",
    typeAnimated: true,
    cancelButtonClass: "btn-primary",
    draggable: true,
    dragWindowBorder: false,
    buttons: {
      info: {
        text: "Si",
        btnClass: "btn-primary",
        action: function () {
          $.ajax({
            url: url, //window.location.pathname
            type: "POST",
            data: parameters,
            dataType: "json",
          })
            .done(function (data) {
              console.log(data);
              if (!data.hasOwnProperty("error")) {
                callback();
                return false;
              }
              alert_error(data.error);
            })
            .fail(function (jqXHR, textStatus, errorThrown) {
              alert(textStatus + ": " + errorThrown);
            })
            .always(function (data) {});
        },
      },
      danger: {
        text: "No",
        btnClass: "btn-red",
        action: function () {},
      },
    },
  });
}
