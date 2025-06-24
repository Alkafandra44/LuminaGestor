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


$(function() {
    // Deshabilitar el campo cliente
    $('#id_cliente').attr('readonly', true)
    .addClass('cliente-readonly')
    .css('pointer-events', 'none');

    // Mostrar el cursor de "no permitido" y un tooltip
    $('#id_cliente').on('mouseenter', function() {
        $(this).css('cursor', 'not-allowed');
        $(this).attr('title', 'No se puede modificar el cliente');
    }).on('mouseleave', function() {
        $(this).css('cursor', 'not-allowed');
    });
});

$(document).on('input', 'textarea[name="respuesta"]', function() {
    this.value = this.value.replace(/[^A-Za-z0-9áéíóúñÁÉÍÓÚÑ\s.,/#]/g, '');
    if (this.value.length > 0) {
        this.value = this.value.charAt(0).toUpperCase() + this.value.slice(1);
    }
});

function validateRespuestaFormSwal() {
    let errors = [];
    const respuesta = $('textarea[name="respuesta"]').val();
    const evaluacion = $('select[name="evaluacion_gestion"]').val();
    const resultado = $('select[name="resultado_gestion"]').val();

    // Respuesta
    if (!/^[A-Za-z0-9áéíóúñÁÉÍÓÚÑ\s.,/#]+$/.test(respuesta) || respuesta.length <= 50) {
        errors.push('La respuesta debe tener al menos 5 caracteres y solo puede contener letras, números y los caracteres ., / #');
    }
    // Evaluacion
    if (!evaluacion) {
        errors.push('Debe seleccionar una evaluación de la gestión.');
    }
    // Resultado
    if (!resultado) {
        errors.push('Debe seleccionar un resultado de la gestión.');
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

// Validación al submit
$(function() {
    $('#formRespuesta').on('submit', function(e) {
        if (!validateRespuestaFormSwal()) {
            e.preventDefault();
            return false;
        }
    });
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
  $(document).on("click", '.btnPrint', function (e) {
    e.preventDefault();
    const respuestaId = $(this).data("respuesta-id");
    if (!respuestaId) {
      alert("No existe respuesta para imprimir");
      return;
    }
    // Descarga directa del PDF
    fetch(`/gestion/respuesta/pdf/${respuestaId}/`, {
      method: "GET",
      headers: {
        "X-Requested-With": "XMLHttpRequest"
      }
    })
      .then(response => {
        if (!response.ok) throw new Error("Error al generar PDF");
        return response.blob();
      })
      .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "respuesta.pdf";
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
      })
      .catch(err => alert(err));
  });
});
