$(document).ready(function () {
    $("#FormTestPaciente").validate({
        rules: {
            'pref_genero': { // <-- Nota las comillas simples
                required: true,
            },
            'tipo_terapia': {
                required: true,
            },
            'pref_corriente': {
                required: true,
            },
            'diagnostico_sospecha': {
                required: true,
            },
            'motivo_busqueda': {
                required: true,
            },
            'rango_precio': {
                required: true,
            },
            'cobertura_salud': {
                required: true,
            },
        },
        messages: {
            'pref_genero': {
                required: "Por favor, selecciona al menos una opción de género.",
            },
            'tipo_terapia': {
                required: "Por favor, selecciona al menos un tipo de terapia.",
            },
            'pref_corriente': {
                required: "Por favor, selecciona al menos una corriente teórica.",
            },
            'diagnostico_sospecha': {
                required: "Por favor, selecciona al menos una opción de diagnóstico.",
            },
            'motivo_busqueda': {
                required: "Por favor, selecciona al menos un motivo de búsqueda.",
            },
            'rango_precio': {
                required: "Por favor, selecciona un rango de precio.",
            },
            'cobertura_salud': {
                required: "Por favor, selecciona una opción de cobertura de salud.",
            },
        },
        errorPlacement: function(error, element) {
            // Coloca el mensaje de error después del elemento contenedor
            error.insertAfter(element.closest('.form-group')); 
        },
        submitHandler: function(form) {
            form.submit();
        }
    });
});

