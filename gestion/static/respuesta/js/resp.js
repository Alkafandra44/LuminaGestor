$(document).ready(function () {
  $("#tblRespuestasClientes").DataTable({
    responsive: true,
    paging: false,
    searching: false,
    info: false,
    ordering: false,
    language: {
      emptyTable: "No hay datos disponibles",
    },
  });
});

$(document).ready(function () {
  // Evento para nueva respuesta
  $(".btnNuevaRespuesta").on("click", function (e) {
    e.preventDefault();
    $("#formRespuesta")[0].reset();

    const expedienteId = $(this).data("expediente-id");
    const clienteId = $(this).data("cliente-id");

    // Configurar modal para nueva respuesta
    $("#modalRespuestaTitle").text("Nueva Respuesta");
    $("input[name='action']").val("add_resp");
    $("#expediente").val(expedienteId);
    $("#id_cliente").val(clienteId);
    $("#respuesta").val("");
    $("#evaluacion_gestion").val("");
    $("#resultado_gestion").val("");
    $("#fecha_respuesta").val(new Date().toISOString().split("T")[0]);

    $('form')[0].reset();
    $("#modalRespuesta").modal("show");
  });

  // Evento para editar respuesta
  $(document).on("click", '.btnEditResp' , function (e) {
    e.preventDefault();
    const respuestaId = $(this).data("respuesta-id");
    if (!respuestaId) {
      alert("No existe respuesta para editar");
      return;
    }

    // Obtener datos de la respuesta por Ajax
    $.ajax({
      url: window.location.pathname,
      type: "GET",
      data: { respuesta_id: respuestaId },
      success: function (response) {
        if (response.success) {
          // Configurar modal para editar
          $("#modalRespuestaTitle").text("Editar Respuesta");
          $("input[name='action']").val("edit_resp");
          $("#id_respuesta_id").val(response.data.id);
          $("#expediente_id").val(response.data.id_expediente);
          $("#id_cliente").val(response.data.cliente_id);
          $("#id_respuesta").val(response.data.respuesta);
          $("#id_evaluacion_gestion").val(response.data.evaluacion_gestion);
          $("#id_resultado_gestion").val(response.data.resultado_gestion);
          $("#fecha_respuesta").val(response.data.fecha_respuesta);

          $('form')[0].reset();
          $("#modalRespuesta").modal("show");
        } else {
          alert("Error al cargar la respuesta: " + response.error);
        }
      },
      error: function() {
        alert("Error en la solicitud");
      }
    });
  });

  // Evento para imprimir
  $(".btnPrint").on("click", function (e) {
    e.preventDefault();
    const respuestaId = $(this).data("respuesta-id");

    if (!respuestaId) {
      alert("No existe respuesta para imprimir");
      return;
    }

    // Configurar botón de impresión
    $("#btnImprimirPDF").attr(
      "href",
      "/gestion/respuesta/print/" + respuestaId + "/"
    );
    $("#modalImprimir").modal("show");
  });

});
