$(document).ready(function () {
    var validator = $("#FormRegistro").validate({
        // ignore: ":hidden",  
        rules: {
            username: {
                required: true,
            },
            first_name: {
                required: true,
            },
            last_name: {
                required: true,
            },
            apellido_materno: {
                required: true,
            },
            genero_idgenero: {
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
            password2: {
                required: true,
                equalTo: "#password",
            },
        },
        messages: {
            username: {
                required: "Su nombre de usuario es un campo obligatorio",
            },
            first_name: {
                required: "Su nombre es un campo obligatorio",
            },
            last_name: {
                required: "Su apellido es un campo obligatorio",
            },
            apellido_materno: {
                required: "Su apellido es un campo obligatorio",
            },
            genero_idgenero: {
                required: "Su género es un campo obligatorio",
            },
            email: {
                required: "El correo es un campo obligatorio",
                email: "El correo no cumple con el formato",
            },
            password: {
                required: "La contraseña es una campo obligatorio",
                minlength: "Mínimo 8 caracteres",
            },
            password2: {
                required: "Repita la contraseña anterior",
                equalTo: "Debe ser igual a la contraseña anterior",
            },
        },
        submitHandler: function(form) {
            form.submit();
        }
    });

    // function onSubmit(token) {
    //     document.getElementById("FormRegistro").submit();
    // }

document.addEventListener('DOMContentLoaded', function() {
        var btnCliente = document.querySelector('.btn-cliente');
        var btnPsicologo = document.querySelector('.btn-psicologo');
        var camposPsicologo = document.getElementById('campos-psicologo');

        camposPsicologo.style.display = 'none';

        function toggleCamposPsicologo() {
            if (btnPsicologo.classList.contains('active')) {
                camposPsicologo.style.display = 'block';
            } else {
                camposPsicologo.style.display = 'none';
            }
            // validator.resetForm();  

        btnCliente.addEventListener('click', function() {
            btnCliente.classList.add('active');
            btnPsicologo.classList.remove('active');
            toggleCamposPsicologo();
        });

        btnPsicologo.addEventListener('click', function() {
            btnCliente.classList.remove('active');
            btnPsicologo.classList.add('active');
            toggleCamposPsicologo();
            });
        }
    });
});


