// Archivo main.js para el Sistema POS

// Función para mostrar tooltips de Bootstrap
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar todos los tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-cerrar alertas después de 5 segundos
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});

// Función para confirmar eliminación
function confirmarEliminacion(event, mensaje) {
    if (!confirm(mensaje || '¿Está seguro de que desea eliminar este elemento?')) {
        event.preventDefault();
        return false;
    }
    return true;
}

// Función para actualizar el contador de caracteres en textareas
function actualizarContador(textareaId, contadorId, maxLength) {
    const textarea = document.getElementById(textareaId);
    const contador = document.getElementById(contadorId);
    
    if (textarea && contador) {
        textarea.addEventListener('input', function() {
            const caracteresRestantes = maxLength - this.value.length;
            contador.textContent = caracteresRestantes;
            
            if (caracteresRestantes < 20) {
                contador.classList.add('text-danger');
            } else {
                contador.classList.remove('text-danger');
            }
        });
    }
}

// Función para validar formularios
function validarFormulario(formId) {
    const form = document.getElementById(formId);
    
    if (form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        });
    }
}