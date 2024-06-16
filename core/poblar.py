import random
from datetime import date, timedelta
from django.contrib.auth.models import User
from .models import (Administrador, Agenda, Coberturasalud, Corrientepsicologica,
                     Diadisponible, Diagnostico, Estadosesion, Estadousuario,
                     Generopsicologo, Mensaje, Metodopago, Motivosesion,
                     Notificacion, Paciente, Pacientepsicologo, Pago, Psicologo,
                     Rangoetario, Rangoprecio, Resena, Sesion, Superusuario,
                     Test, Testpaciente, Testpsicologo, Ticketsoporte,
                     Tiposesion, Usuario)

def populate_database(num_users=10, num_sessions=50):
    estados_usuario = [
        Estadousuario(estadousuario='Activo', descripcion='Usuario activo'),
        Estadousuario(estadousuario='Inactivo', descripcion='Usuario inactivo')
    ]
    Estadousuario.objects.bulk_create(estados_usuario)

    tipos_sesion = [
        Tiposesion(nombre='Individual', descripcion='Aborda desafíos personales con un terapeuta.'),
        Tiposesion(nombre='Pareja', descripcion='Enfoca conflictos y mejoras en la relación.'),
        Tiposesion(nombre='Familiar', descripcion='Trabaja en dinámicas y comunicación familiar.')
    ]
    Tiposesion.objects.bulk_create(tipos_sesion)

    metodos_pago = [
        Metodopago(metodopago='Tarjeta de credito', descripcion='Pago con tarjeta de credito', habilitado='S'),
        Metodopago(metodopago='Paypal', descripcion='Pago con Paypal', habilitado='S'),
        Metodopago(metodopago='Efectivo', descripcion='Pago en efectivo', habilitado='N')
    ]
    Metodopago.objects.bulk_create(metodos_pago)

    estados_sesion = [
        Estadosesion(nombre='Programada', descripcion='Sesión programada'),
        Estadosesion(nombre='Completada', descripcion='Sesión completada'),
        Estadosesion(nombre='En curso', descripcion='Sesión en curso'),
        Estadosesion(nombre='Cancelada', descripcion='Sesión cancelada')
    ]
    Estadosesion.objects.bulk_create(estados_sesion)

    generos_psicologo = [
        Generopsicologo(idgeneropsicologo=1, genero='Masculino'),
        Generopsicologo(idgeneropsicologo=2, genero='Femenino'),
        Generopsicologo(idgeneropsicologo=3, genero='Otro')
    ]
    Generopsicologo.objects.bulk_create(generos_psicologo)

    rangos_etarios = [
        Rangoetario(idrangoetario=1, rangoetario='0-18'),
        Rangoetario(idrangoetario=2, rangoetario='19-30'),
        Rangoetario(idrangoetario=3, rangoetario='31-50'),
        Rangoetario(idrangoetario=4, rangoetario='51+'),
    ]
    Rangoetario.objects.bulk_create(rangos_etarios)

    rangos_precios = [
        Rangoprecio(idrangoprecio=1, montominimo=0, montomaximo=50),
        Rangoprecio(idrangoprecio=2, montominimo=51, montomaximo=100),
        Rangoprecio(idrangoprecio=3, montominimo=101, montomaximo=200),
    ]
    Rangoprecio.objects.bulk_create(rangos_precios)

    coberturas_salud = [
        Coberturasalud(idcoberturasalud=1, coberturasalud='Cobertura A'),
        Coberturasalud(idcoberturasalud=2, coberturasalud='Cobertura B'),
        Coberturasalud(idcoberturasalud=3, coberturasalud='Cobertura C'),
    ]
    Coberturasalud.objects.bulk_create(coberturas_salud)

    diagnosticos = [
        Diagnostico(diagnostico='Ansiedad', descripcion='Descripción de Ansiedad'),
        Diagnostico(diagnostico='Depresión', descripcion='Descripción de Depresión'),
        Diagnostico(diagnostico='Estrés', descripcion='Descripción de Estrés'),
    ]
    Diagnostico.objects.bulk_create(diagnosticos)

    corrientes_psicologicas = [
        Corrientepsicologica(corrientepsicologica='Cognitivo Conductual', descripcion='Descripción de Cognitivo Conductual'),
        Corrientepsicologica(corrientepsicologica='Psicoanálisis', descripcion='Descripción de Psicoanálisis'),
        Corrientepsicologica(corrientepsicologica='Humanista', descripcion='Descripción de Humanista'),
    ]
    Corrientepsicologica.objects.bulk_create(corrientes_psicologicas)

    motivos_sesion = [
        Motivosesion(motivosesion='Ansiedad', descripcion='Descripción de Ansiedad'),
        Motivosesion(motivosesion='Depresión', descripcion='Descripción de Depresión'),
        Motivosesion(motivosesion='Manejo del estrés', descripcion='Descripción de Manejo del estrés'),
    ]
    Motivosesion.objects.bulk_create(motivos_sesion)

    # Create users
    users = []
    for i in range(num_users):
        user = User.objects.create_user(f'user{i}', f'user{i}@example.com', 'password')
        usuario = Usuario(
            user=user,
            telefono=f'123-456-789{i}',
            estadousuario_idestadousuario=random.choice(estados_usuario),
            tipousuario='paciente' if i % 2 == 0 else 'psicologo'
        )
        usuario.save()
        users.append(usuario)

        if usuario.tipousuario == 'paciente':
            Paciente.objects.create(pac_idusuario=usuario)
        else:
            Psicologo.objects.create(
                psi_idusuario=usuario,
                idcorrientepsicologica=random.choice(corrientes_psicologicas),
                iddiagnostico=random.choice(diagnosticos),
                idmotivosesion=random.choice(motivos_sesion),
                tarifasesion=random.randint(50, 150)
            )

    # Create entities related to users and other independent tables
    for usuario in users:
        if usuario.tipousuario == 'paciente':
            Test.objects.create(
                generopsicologo_idgeneropsicologo=random.choice(generos_psicologo),
                rangoetario_idrangoetario=random.choice(rangos_etarios),
                corrientepsicologica_idcorrientepsicologica=random.choice(corrientes_psicologicas),
                rangoprecio_idrangoprecio=random.choice(rangos_precios),
                motivosesion_idmotivosesion=random.choice(motivos_sesion),
                coberturasalud_idcoberturasalud=random.choice(coberturas_salud),
                diagnostico_iddiagnostico=random.choice(diagnosticos),
                tiposesion_idtiposesion=random.choice(tipos_sesion),
                idusuariotest=usuario
            )
        elif usuario.tipousuario == 'psicologo':
            agenda = Agenda.objects.create(
                notasadicionales=f'Notas adicionales para la agenda de {usuario}',
                usuario_idusuario=usuario
            )
            for j in range(random.randint(1, 5)):
                Diadisponible.objects.create(
                    fechahora=date.today() + timedelta(days=random.randint(1, 30)),
                    agenda_idagenda=agenda
                )

    # Create Sesion and related entities after users are created
    for i in range(num_sessions):
        paciente = random.choice([u for u in users if u.tipousuario == 'paciente'])
        psicologo = random.choice([u for u in users if u.tipousuario == 'psicologo'])

        sesion = Sesion.objects.create(
            fechahora=date.today() + timedelta(days=random.randint(-30, 30)),
            notas=f'Notas de la sesion {i}',
            estadosesion_idestadosesion=random.choice(estados_sesion),
            tiposesion_idtiposesion=random.choice(tipos_sesion),
            usuario_idusuario=paciente
        )

        Pago.objects.create(
            fechahora=sesion.fechahora,
            montototal=random.randint(50, 150),
            sesion_idsesion=sesion,
            metodopago_idmetodopago=random.choice(metodos_pago)
        )

        # ... (Rest of the code remains similar, creating instances for other tables)

if __name__ == '__main__':
    populate_database()
