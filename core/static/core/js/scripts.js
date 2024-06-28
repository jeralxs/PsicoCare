

$(document).ready(function(){

    $("#IngresarForm").validate({
        rules: {
            username: {
                required: true,
            },
            password:{
                required: true,
            },
        },
        messages: {
            username: {
                required: "El usuario es obligatorio",
            },
            password: {
                required: "La contraseña es obligatoria"
            },
        },
        submitHandler: function(form) {
            form.submit();
        }
    });
});


$(document).ready(function () {
    $("#DatosPersonalesForm").validate({
        rules: {
            username: {
                required: true,
            },
            nombres: {
                required: true,
            },
            apellido_paterno: {
                required: true,
            },
            apellido_materno: {
                required: true,
            },
            email: {
                required: true,
                email: true,
            },
            password: {
                 required: true,
                 minlength: 8,
            },
        },
        messages: {
            username: {
                required: "Su nombre de usuario es un campo obligatorio",
            },
            nombres: {
                required: "Su nombre es un campo obligatorio",
            },
            apellido_paterno: {
                required: "Su apellido es un campo obligatorio",
            },
            apellido_materno: {
                required: "Su apellido es un campo obligatorio",
            },
            email: {
                required: "El correo es un campo obligatorio",
                email: "El correo no cumple con el formato",
            },
            password: {
                required: "La contraseña es obligatoria",
                minlength: "Mínimo 8 caracteres",
           },
        },
        submitHandler: function(form) {
            form.submit();
        }
    });
});


$(document).ready(function(){

    $("#EliminarForm").validate({
        rules: {
            password:{
                required: true,
            },
        },
        messages: {
            password: {
                required: "Debe ingresar la contraseña"
            },
        },
        submitHandler: function(form) {
            form.submit();
        }
    });
});

$(document).ready(function () {
    $("#DatosProfesionalesForm").validate({
        rules: {
            rango_etario: {
                required: true,
            },
            corriente_psicologica: {
                required: true,
            },
            esp_diagnostica: {
                required: true,
            },
            areas_trabajo: {
                required: true,
            },
            rango_precio: {
                required: true,
            },
            cobertura_aceptada: {
                required: true,
            },
            numeroregistrolicencia: {
                required: true,
            },
        },
        messages: {
            rango_etario: {
                required: "El rango etario es un campo obligatorio",
            },
            corriente_psicologica: {
                required: "Por favor seleccione al menos una opción",
            },
            esp_diagnostica: {
                required: "La especialidad diagnóstica es un campo obligatorio",
            },
            areas_trabajo: {
                required: "Las áreas con las que trabaja son un campo obligatorio",
            },
            rango_precio: {
                required: "El rango de precio es un campo obligatorio",
            },
            cobertura_aceptada: {
                required: "Por favor seleccione al menos una opción",
            },
            numeroregistrolicencia: {
                required: "Su número de licencia es un campo obligatorio",
            },
        },
        submitHandler: function(form) {
            form.submit();
        }
    });
});

//test paciente matching



$('body').on('click', '.test-next', function() { 
    var id = $('.content-test:visible').data('id');
    var nextId = $('.content-test:visible').data('id')+1;
    $('[data-id="'+id+'"]').hide();
    $('[data-id="'+nextId+'"]').show();

    if($('.test-back:hidden').length == 1){
        $('.test-back').show();
    }

    if(nextId == 9){
        $('.test-paciente').hide();
        $('.test-paciente-end').show();
    }
});

$('body').on('click', '.test-back', function() { 
    var id = $('.content-test:visible').data('id');
    var prevId = $('.content-test:visible').data('id')-1;
    $('[data-id="'+id+'"]').hide();
    $('[data-id="'+prevId+'"]').show();

    if(prevId == 1){
        $('.test-back').hide();
    }    
});

$('body').on('click', '.edit-anterior', function() { 
    $('.test-paciente-end').hide();
    $('.test-paciente').show();
    $('#content-8').show();
});

//test paciente matching end

