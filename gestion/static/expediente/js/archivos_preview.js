document.addEventListener('DOMContentLoaded', function() {
    const inputArchivos = document.getElementById('id_archivos');
    const preview = document.getElementById('preview-archivos');
    let archivosSeleccionados = [];

    inputArchivos.addEventListener('change', function(e) {
        archivosSeleccionados = Array.from(e.target.files);
        mostrarVistaPrevia();
    });

    function mostrarVistaPrevia() {
        preview.innerHTML = '';
        if (archivosSeleccionados.length === 0) {
            preview.innerHTML = '<span class="text-muted">No hay archivos seleccionados.</span>';
            return;
        }
        const ul = document.createElement('ul');
        ul.className = 'list-group';
        archivosSeleccionados.forEach((archivo, idx) => {
            const li = document.createElement('li');
            li.className = 'list-group-item d-flex align-items-center';
            // Checkbox
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.checked = true;
            checkbox.disabled = true;
            checkbox.className = 'me-2';
            li.appendChild(checkbox);
            // Miniatura si es imagen
            if (archivo.type.startsWith('image/')) {
                const img = document.createElement('img');
                img.src = URL.createObjectURL(archivo);
                img.style.height = '40px';
                img.style.marginRight = '10px';
                li.appendChild(img);
            } else {
                const icon = document.createElement('i');
                icon.className = 'fas fa-file me-2';
                li.appendChild(icon);
            }
            // Nombre del archivo
            li.appendChild(document.createTextNode(archivo.name));
            // Botón para quitar
            const btnQuitar = document.createElement('button');
            btnQuitar.type = 'button';
            btnQuitar.className = 'btn btn-danger btn-sm ms-auto';
            btnQuitar.innerHTML = '<i class="fas fa-times"></i>';
            btnQuitar.onclick = function() {
                archivosSeleccionados.splice(idx, 1);
                actualizarInputArchivos();
                mostrarVistaPrevia();
            };
            li.appendChild(btnQuitar);
            ul.appendChild(li);
        });
        preview.appendChild(ul);
    }

    function actualizarInputArchivos() {
        // Crear un nuevo DataTransfer para actualizar el input file
        const dt = new DataTransfer();
        archivosSeleccionados.forEach(file => dt.items.add(file));
        inputArchivos.files = dt.files;
    }
});

$(document).on('click', '.btnEliminarArchivo', function() {
    var archivoId = $(this).data('archivo-id');
    var $btn = $(this);
    Swal.fire({
        title: '¿Estás seguro?',
        text: "¡Esta acción eliminará el archivo!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, eliminar'
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                url: window.location.pathname, // La misma URL de la vista de edición
                type: 'POST',
                data: {
                    action: 'delete_archivo',
                    archivo_id: archivoId,
                },
                success: function(response) {
                    if (response.success) {
                        $btn.closest('li').remove();
                        Swal.fire('Eliminado', 'El archivo ha sido eliminado.', 'success');
                    } else {
                        Swal.fire('Error', response.error || 'No se pudo eliminar el archivo.', 'error');
                    }
                }
            });
        }
    });
});