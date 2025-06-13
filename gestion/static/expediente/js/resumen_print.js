document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("btnPrintResumen").addEventListener("click", function () {
        const resumen = document.getElementById("id_resumen").value;
        const formData = new FormData();
        formData.append("resumen", resumen);

        fetch(resumenPdfUrl, {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
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
            a.download = "resumen.pdf";
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
        })
        .catch(err => alert(err));
    });
});