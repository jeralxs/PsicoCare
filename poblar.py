import random
from datetime import date, timedelta
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PsicoCare.settings') 
django.setup()

from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import connections
from core.models import (Administrador, Agenda, Coberturasalud, Corrientepsicologica,
                     Diadisponible, Diagnostico, Estadosesion, Estadousuario,
                     Genero, Generopsicologo, Mensaje, Metodopago, Motivosesion,
                     Notificacion, Paciente, Pacientepsicologo, Pago, Psicologo,
                     Rangoetario, Rangoprecio, Resena, Superusuario,
                     Test, Testpaciente, Testpsicologo, Ticketsoporte,
                     Tiposesion, Usuario)

def drop_sequences(cursor):
    sequences = [
        "usuario_seq", "agenda_seq", "coberturassalud_seq", 
        "corrientepsicologica_seq", "diadisponible_seq", "diagnostico_seq", 
        "estadosesion_seq", "estadousuario_seq", "genero_seq", 
        "generopsicologo_seq", "mensaje_seq", "metodopago_seq", 
        "motivosesion_seq", "notificacion_seq", "paciente_seq", 
        "pacientepsicologo_seq", "pago_seq", "psicologo_seq", 
        "rangoetario_seq", "rangoprecio_seq", "resena_seq", 
        "sesion_seq", "test_seq", "testpaciente_seq", 
        "testpsicologo_seq", "ticketsoporte_seq", "tiposesion_seq"
    ]
    for seq_name in sequences:
        cursor.execute(f"SELECT sequence_name FROM user_sequences WHERE sequence_name = '{seq_name.upper()}'")
        sequence_exists = cursor.fetchone()

        if not sequence_exists:
            # Si no existe
            print(f"Secuencia {seq_name} NO EXISTE.")
        else:
            cursor.execute(f"DROP SEQUENCE {seq_name}")
            print(f"Secuencia {seq_name} ELIMINADA.")
def create_sequences(cursor):
    sequences = [
        "usuario_seq", "agenda_seq", "coberturassalud_seq", 
        "corrientepsicologica_seq", "diadisponible_seq", "diagnostico_seq", 
        "estadosesion_seq", "estadousuario_seq", "genero_seq", 
        "generopsicologo_seq", "mensaje_seq", "metodopago_seq", 
        "motivosesion_seq", "notificacion_seq", "paciente_seq", 
        "pacientepsicologo_seq", "pago_seq", "psicologo_seq", 
        "rangoetario_seq", "rangoprecio_seq", "resena_seq", 
        "sesion_seq", "test_seq", "testpaciente_seq", 
        "testpsicologo_seq", "ticketsoporte_seq", "tiposesion_seq"
    ]
    for seq_name in sequences:
        # Verificar si la secuencia ya existe en Oracle
        cursor.execute(f"SELECT sequence_name FROM user_sequences WHERE sequence_name = '{seq_name.upper()}'")
        sequence_exists = cursor.fetchone()

        if not sequence_exists:
            # Si no existe, crear la secuencia en Oracle
            cursor.execute(f"CREATE SEQUENCE {seq_name} START WITH 1 INCREMENT BY 1 NOCACHE")
            print(f"Secuencia {seq_name} creada.")
        else:
            print(f"La secuencia {seq_name} ya existe en la base de datos.")

def clean_database(cursor):
    try:
        print('Elimininar tablas')
        tables = [
            'administrador', 'superusuario','appointment', 'schedule','paciente','psicologo','usuario','estadosesion', 
            'generopsicologo','rangoetario', 'corrientepsicologica', 'rangoprecio', 'motivosesion', 
            'coberturasalud', 'diagnostico', 'tiposesion', 'metodopago','agenda', 'diadisponible', 
            'mensaje', 'notificacion',
                'pacientepsicologo',
                  'pago',
             'test', 'testpaciente', 'testpsicologo', 'ticketsoporte', 
            'resena', 'sesion', 'estadousuario','genero', 'core_conversation', 'auth_user'
        ]

        for table in tables:
            cursor.execute(f"DELETE FROM {table}")
            print(f"Datos de la tabla {table} eliminados.")
    except Exception as err:
        print(f"    Error: {err}")
    
def get_next_sequence_value(cursor, sequence_name):
    cursor.execute(f"SELECT {sequence_name}.NEXTVAL FROM DUAL")
    return cursor.fetchone()[0]

def crear_usuario(idusuario, username, tipo, genero, nombre, apellido, apellido_m, telefono, correo, es_superusuario, 
    es_staff, estado, foto, idpaciente, idpsicologo, rango_etario, corriente, precio, motivo, cobertura, diagnostico, tiposesion, bio):

    try:
        print(f'Verificar si existe usuario {username}.')

        if User.objects.filter(username=username).exists():
            print(f'   Eliminar {username}')
            User.objects.get(username=username).delete()
            print(f'   Eliminado {username}')
        
        print(f'Iniciando creación de usuario {username}.')

        usuario = None
        if tipo == 'superusuario':
            print('    Crear Superuser')
            usuario = User.objects.create_superuser(username=username, password='psicocare123')
        else:
            print('    Crear User')
            usuario = User.objects.create_user(username=username, password='user123')

        if tipo == 'administrador':
            print('    Es administrador')
            usuario.is_staff = es_staff
            
        usuario.first_name = nombre
        usuario.last_name = apellido
        usuario.email = correo
        usuario.save()

        if tipo == 'administrador':
            print(f'    Dar permisos a core y apirest')
            permisos = Permission.objects.filter(content_type__app_label__in=['core', 'apirest'])
            usuario.user_permissions.set(permisos)
            usuario.save()
 
        print(f'    Crear usuario: {username}')
        usuario=Usuario.objects.create(
            idusuario=idusuario,
            user=usuario,
            genero_idgenero = genero,
            foto = foto,
            apellido_materno = apellido_m,
            telefono = telefono,
            estadousuario_idestadousuario = estado,
            tipousuario = tipo)
        print("    Creado correctamente")

        if tipo == 'paciente':
            print(f'    Crear paciente: {username}')
            Paciente.objects.create(
                idpaciente = idpaciente,
                pac_idusuario = usuario)
        
        if tipo == 'psicologo':
            print(f'    Crear psicologo: {username}')
            Psicologo.objects.create(
                idpsicologo = idpsicologo,
                bio_info = bio,
                psi_idusuario = usuario,
                rangoetario_idrangoetario= rango_etario,
                corriente_idcorriente= corriente,
                rangoprecio_idrangoprecio= precio,
                motivosesion_idmotivosesion= motivo,
                coberturasalud_id=cobertura,
                diagnostico_iddiagnostico=diagnostico,
                tiposesion_idtiposesion=tiposesion,
                numeroregistrolicencia=random.randint(100000, 999999),)

    except Exception as err:
        print(f"    Error: {err}")

def populate_database():
    # Get Oracle connection
    cursor = connections['default'].cursor()

    clean_database(cursor)
    # Crear secuencias
    drop_sequences(cursor)
    create_sequences(cursor)
    

    # Create data for independent tables
    estados_usuario = [
        Estadousuario(idestadousuario=get_next_sequence_value(cursor, 'estadousuario_seq'), estadousuario='Activo', descripcion='Usuario activo en la plataforma'),
        Estadousuario(idestadousuario=get_next_sequence_value(cursor, 'estadousuario_seq'), estadousuario='Inactivo', descripcion='Usuario inactivo en la plataforma'),
    ]
    Estadousuario.objects.bulk_create(estados_usuario)

    generos = [
        Genero(idgenero=get_next_sequence_value(cursor, 'genero_seq'), n_genero='Masculino'),
        Genero(idgenero=get_next_sequence_value(cursor, 'genero_seq'), n_genero='Femenino'),
        Genero(idgenero=get_next_sequence_value(cursor, 'genero_seq'), n_genero='No binario'),
        Genero(idgenero=get_next_sequence_value(cursor, 'genero_seq'), n_genero='Prefiero no decir'),
    ]
    Genero.objects.bulk_create(generos)

    coberturas_salud = [
        Coberturasalud(idcoberturasalud=get_next_sequence_value(cursor, 'coberturassalud_seq'), coberturasalud='Fonasa'),
        Coberturasalud(idcoberturasalud=get_next_sequence_value(cursor, 'coberturassalud_seq'), coberturasalud='Isapre'),
        Coberturasalud(idcoberturasalud=get_next_sequence_value(cursor, 'coberturassalud_seq'), coberturasalud='Otra'),
        Coberturasalud(idcoberturasalud=get_next_sequence_value(cursor, 'coberturassalud_seq'), coberturasalud='Ninguna'),
    ]
    Coberturasalud.objects.bulk_create(coberturas_salud)

    corrientes_psicologicas = [
        Corrientepsicologica(idcorrientepsicologica=get_next_sequence_value(cursor, 'corrientepsicologica_seq'), corrientepsicologica='Cognitivo Conductual', descripcion='Aborda cómo los pensamientos y comportamientos afectan la salud mental.'),
        Corrientepsicologica(idcorrientepsicologica=get_next_sequence_value(cursor, 'corrientepsicologica_seq'), corrientepsicologica='Psicoanálisis', descripcion='Explora el inconsciente y la influencia del pasado en el presente.'),
        Corrientepsicologica(idcorrientepsicologica=get_next_sequence_value(cursor, 'corrientepsicologica_seq'), corrientepsicologica='Sistémica', descripcion='Analiza las interacciones y relaciones dentro de sistemas sociales.'),
        Corrientepsicologica(idcorrientepsicologica=get_next_sequence_value(cursor, 'corrientepsicologica_seq'), corrientepsicologica='Humanista', descripcion='Se enfoca en el crecimiento personal y el potencial humano.'),
        Corrientepsicologica(idcorrientepsicologica=get_next_sequence_value(cursor, 'corrientepsicologica_seq'), corrientepsicologica='Breve', descripcion='Se centra en soluciones prácticas y cambios rápidos para abordar problemas específicos.'),
        Corrientepsicologica(idcorrientepsicologica=get_next_sequence_value(cursor, 'corrientepsicologica_seq'), corrientepsicologica='Feminista', descripcion='Destaca el género y el poder en la construcción de identidades.'),
        Corrientepsicologica(idcorrientepsicologica=get_next_sequence_value(cursor, 'corrientepsicologica_seq'), corrientepsicologica='Sin preferencia', descripcion='No tiene preferencias sobre alguna corriente psicológica en particular.'),
    ]
    Corrientepsicologica.objects.bulk_create(corrientes_psicologicas)

    diagnosticos = [
        Diagnostico(iddiagnostico=get_next_sequence_value(cursor, 'diagnostico_seq'), diagnostico='Ansiedad', descripcion='Exceso de preocupación y miedo.'),
        Diagnostico(iddiagnostico=get_next_sequence_value(cursor, 'diagnostico_seq'), diagnostico='Autolesiones', descripcion='Daño intencionado al propio cuerpo.'),
        Diagnostico(iddiagnostico=get_next_sequence_value(cursor, 'diagnostico_seq'), diagnostico='Bipolaridad', descripcion='Cambios extremos de estados de ánimo (depresión y manía).'),
        Diagnostico(iddiagnostico=get_next_sequence_value(cursor, 'diagnostico_seq'), diagnostico='Consumo problemático', descripcion='Uso excesivo de sustancias.'),
        Diagnostico(iddiagnostico=get_next_sequence_value(cursor, 'diagnostico_seq'), diagnostico='Crisis de pánico', descripcion='Ataques repentinos de miedo intenso.'),
        Diagnostico(iddiagnostico=get_next_sequence_value(cursor, 'diagnostico_seq'), diagnostico='Depresión', descripcion='Sentimientos persistentes de tristeza y desesperanza o desinterés general.'),
        Diagnostico(iddiagnostico=get_next_sequence_value(cursor, 'diagnostico_seq'), diagnostico='Disfunciones sexuales', descripcion='Problemas en la función sexual.'),
        Diagnostico(iddiagnostico=get_next_sequence_value(cursor, 'diagnostico_seq'), diagnostico='Neurodivergencia', descripcion='Neurología atípica'),
        Diagnostico(iddiagnostico=get_next_sequence_value(cursor, 'diagnostico_seq'), diagnostico='Riesgo suicida', descripcion='Tendencias o pensamientos suicidas.'),  
        Diagnostico(iddiagnostico=get_next_sequence_value(cursor, 'diagnostico_seq'), diagnostico='Trastorno disociativo', descripcion='Desconexión de pensamientos, sensaciones o identidad.'),
        Diagnostico(iddiagnostico=get_next_sequence_value(cursor, 'diagnostico_seq'), diagnostico='Trastorno de estrés postraumático', descripcion='Respuesta a eventos traumáticos.'),
        Diagnostico(iddiagnostico=get_next_sequence_value(cursor, 'diagnostico_seq'), diagnostico='Trastorno de conducta alimentaria', descripcion='Relación disfuncional con la comida.'),
        Diagnostico(iddiagnostico=get_next_sequence_value(cursor, 'diagnostico_seq'), diagnostico='Trastorno de personalidad', descripcion='Patrones de comportamiento inflexibles fuera de la norma social.'),
        Diagnostico(iddiagnostico=get_next_sequence_value(cursor, 'diagnostico_seq'), diagnostico='Otro', descripcion='Cualquier otro diagnóstico no especificado.'),
        Diagnostico(iddiagnostico=get_next_sequence_value(cursor, 'diagnostico_seq'), diagnostico='Sin diagnostico', descripcion='No tiene algún diagnostico'),
    ]
    Diagnostico.objects.bulk_create(diagnosticos)

    rangos_precio = [
        Rangoprecio(idrangoprecio=get_next_sequence_value(cursor, 'rangoprecio_seq'), montominimo=0, montomaximo=5000 ),
        Rangoprecio(idrangoprecio=get_next_sequence_value(cursor, 'rangoprecio_seq'), montominimo=5001, montomaximo=10000 ),
        Rangoprecio(idrangoprecio=get_next_sequence_value(cursor, 'rangoprecio_seq'), montominimo=10001, montomaximo=15000 ),
        Rangoprecio(idrangoprecio=get_next_sequence_value(cursor, 'rangoprecio_seq'), montominimo=15001, montomaximo=20000 ),
        Rangoprecio(idrangoprecio=get_next_sequence_value(cursor, 'rangoprecio_seq'), montominimo=20001, montomaximo=25000),
        Rangoprecio(idrangoprecio=get_next_sequence_value(cursor, 'rangoprecio_seq'), montominimo=25001, montomaximo=30000),
        Rangoprecio(idrangoprecio=get_next_sequence_value(cursor, 'rangoprecio_seq'), montominimo=30001, montomaximo=35000),
        Rangoprecio(idrangoprecio=get_next_sequence_value(cursor, 'rangoprecio_seq'), montominimo=35001, montomaximo=40000),
        Rangoprecio(idrangoprecio=get_next_sequence_value(cursor, 'rangoprecio_seq'), montominimo=40001, montomaximo=450000),
        Rangoprecio(idrangoprecio=get_next_sequence_value(cursor, 'rangoprecio_seq'), montominimo=45001, montomaximo=50000),
        Rangoprecio(idrangoprecio=get_next_sequence_value(cursor, 'rangoprecio_seq'), montominimo=50001, montomaximo=55000),
        Rangoprecio(idrangoprecio=get_next_sequence_value(cursor, 'rangoprecio_seq'), montominimo=55001, montomaximo=60000),
        Rangoprecio(idrangoprecio=get_next_sequence_value(cursor, 'rangoprecio_seq'), montominimo=60001, montomaximo=65000),
        Rangoprecio(idrangoprecio=get_next_sequence_value(cursor, 'rangoprecio_seq'), montominimo=65001, montomaximo=70000),
    ]
    Rangoprecio.objects.bulk_create(rangos_precio)


    estados_sesion = [
        Estadosesion(idestadosesion=get_next_sequence_value(cursor, 'estadosesion_seq'),nombre='Agendada', descripcion='La sesión está agendada'),
        Estadosesion(idestadosesion=get_next_sequence_value(cursor, 'estadosesion_seq'),nombre='Realizada', descripcion='La sesión se llevó a cabo'),
        Estadosesion(idestadosesion=get_next_sequence_value(cursor, 'estadosesion_seq'),nombre='Cancelada', descripcion='La sesión fue cancelada'),
    ]
    Estadosesion.objects.bulk_create(estados_sesion)

    generos_psicologo = [
        Generopsicologo(idgeneropsicologo=get_next_sequence_value(cursor, 'generopsicologo_seq'),genero='Masculino'),
        Generopsicologo(idgeneropsicologo=get_next_sequence_value(cursor, 'generopsicologo_seq'),genero='Femenino'),
        Generopsicologo(idgeneropsicologo=get_next_sequence_value(cursor, 'generopsicologo_seq'),genero='No binario'),
        Generopsicologo(idgeneropsicologo=get_next_sequence_value(cursor, 'generopsicologo_seq'),genero='Sin preferencia'),
    ]
    Generopsicologo.objects.bulk_create(generos_psicologo)

    metodos_pago = [
        Metodopago(idmetodopago=get_next_sequence_value(cursor, 'metodopago_seq'),metodopago='Efectivo', descripcion='Pago en efectivo', habilitado='S'),
        Metodopago(idmetodopago=get_next_sequence_value(cursor, 'metodopago_seq'),metodopago='Transferencia bancaria', descripcion='Transferencia a cuenta bancaria', habilitado='S'),
        Metodopago(idmetodopago=get_next_sequence_value(cursor, 'metodopago_seq'),metodopago='Webpay', descripcion='Pago a través de webpay', habilitado='S'),
    ]
    Metodopago.objects.bulk_create(metodos_pago)

    motivos_sesion = [
        Motivosesion(idmotivosesion=get_next_sequence_value(cursor, 'motivosesion_seq'),motivosesion='Acoso', descripcion='Hostigamiento persistente o agresión.'),
        Motivosesion(idmotivosesion=get_next_sequence_value(cursor, 'motivosesion_seq'),motivosesion='Bullying', descripcion='Acoso repetido en entornos escolares.'),
        Motivosesion(idmotivosesion=get_next_sequence_value(cursor, 'motivosesion_seq'),motivosesion='Crisis existencial', descripcion='Cuestionamiento profundo de la vida.'),
        Motivosesion(idmotivosesion=get_next_sequence_value(cursor, 'motivosesion_seq'),motivosesion='Duelo', descripcion='Proceso de adaptación a la pérdida.'),
        Motivosesion(idmotivosesion=get_next_sequence_value(cursor, 'motivosesion_seq'),motivosesion='Estrés', descripcion='Respuesta física y emocional a la presión.'),
        Motivosesion(idmotivosesion=get_next_sequence_value(cursor, 'motivosesion_seq'),motivosesion='Problemas vocacionales', descripcion='Confusión o insatisfacción con dirección de estudios o trabajo.'),
        Motivosesion(idmotivosesion=get_next_sequence_value(cursor, 'motivosesion_seq'),motivosesion='Problemas de relaciones', descripcion='Dificultades en interacciones personales.'),
        Motivosesion(idmotivosesion=get_next_sequence_value(cursor, 'motivosesion_seq'),motivosesion='Regulación emocional', descripcion='Problemas con manejo de emociones de manera saludable.'),
        Motivosesion(idmotivosesion=get_next_sequence_value(cursor, 'motivosesion_seq'),motivosesion='Género y/o sexualidad', descripcion='Problemas de identidad u orientación sexual.'),
        Motivosesion(idmotivosesion=get_next_sequence_value(cursor, 'motivosesion_seq'),motivosesion='Autoestima', descripcion='Valoración negativa de uno mismo.'),
        Motivosesion(idmotivosesion=get_next_sequence_value(cursor, 'motivosesion_seq'),motivosesion='No lo sé', descripcion='Problemas para identificar motivo de búsqueda.'),
        Motivosesion(idmotivosesion=get_next_sequence_value(cursor, 'motivosesion_seq'),motivosesion='Otro', descripcion='Motivo no listado.'),
    ]
    Motivosesion.objects.bulk_create(motivos_sesion)

    rangos_etarios = [
        Rangoetario(idrangoetario=get_next_sequence_value(cursor, 'rangoetario_seq'),rangoetario='Niños (0-12 años)'),
        Rangoetario(idrangoetario=get_next_sequence_value(cursor, 'rangoetario_seq'),rangoetario='Adolescentes (13-18 años)'),
        Rangoetario(idrangoetario=get_next_sequence_value(cursor, 'rangoetario_seq'),rangoetario='Adultos (19-59 años)'),
        Rangoetario(idrangoetario=get_next_sequence_value(cursor, 'rangoetario_seq'),rangoetario='Adultos mayores (60+ años)'),
    ]
    Rangoetario.objects.bulk_create(rangos_etarios)


    tipos_sesion = [
        Tiposesion(idtiposesion=get_next_sequence_value(cursor, 'tiposesion_seq'),nombre='Individual', descripcion='Sesión individual con el psicólogo'),
        Tiposesion(idtiposesion=get_next_sequence_value(cursor, 'tiposesion_seq'),nombre='Pareja', descripcion='Sesión para parejas'),
        Tiposesion(idtiposesion=get_next_sequence_value(cursor, 'tiposesion_seq'),nombre='Familiar', descripcion='Sesión para familias'),
    ]
    Tiposesion.objects.bulk_create(tipos_sesion)

    bio = "Lorem ipsum dolor sit amet consectetur, adipiscing elit sociosqu quam suspendisse viverra, leo integer vel torquent. Per cum dignissim rutrum sociis ac montes netus venenatis viverra, magnis platea tincidunt cursus ridiculus id primis iaculis, nascetur quis pulvinar duis mattis lacinia pharetra facilisis. Venenatis netus morbi praesent mi laoreet semper id pharetra sodales, fusce felis conubia aliquet urna habitant ut."
    
    #SUPERUSUARIO
    crear_usuario(get_next_sequence_value(cursor, 'usuario_seq'), 'psicocare', 'superusuario', random.choice(generos), 'admin', 
                  'admin', 'admin', 11111111, 'psicocareduoc@gmail.com', True, True, random.choice(estados_usuario), 'img/fotoperfil.jpg', 
                  '','', '', '', '','', '', '', '',bio)
    #PACIENTES
    crear_usuario(get_next_sequence_value(cursor, 'usuario_seq'), 'paciente1', 'paciente', Genero.objects.get(idgenero=1), 'Pedrito', 
                  'Suárez', 'Monsalves', 11111111, 'psuarez@gmail.com', False, False, random.choice(estados_usuario), 'img/usuario1.jpg', 
                  get_next_sequence_value(cursor, 'paciente_seq'),'','', '', '', '', '', '', '',bio)
    crear_usuario(get_next_sequence_value(cursor, 'usuario_seq'), 'paciente2', 'paciente', Genero.objects.get(idgenero=1), 'Juan', 
                  'Perez', 'Garcia', 11111111, 'jperez@gmail.com', False, False, random.choice(estados_usuario), 'img/usuario2.jpg', 
                  get_next_sequence_value(cursor, 'paciente_seq'),'','', '', '', '', '', '', '',bio)
    crear_usuario(get_next_sequence_value(cursor, 'usuario_seq'), 'paciente3', 'paciente', Genero.objects.get(idgenero=2), 'Maria', 
                  'Henríquez', 'Lopez', 11111111,'mhenriquez@gmail.com', False, False, random.choice(estados_usuario), 'img/usuario3.jpg', 
                  get_next_sequence_value(cursor, 'paciente_seq'),'','', '', '', '', '', '', '',bio)
    crear_usuario(get_next_sequence_value(cursor, 'usuario_seq'), 'paciente4', 'paciente', Genero.objects.get(idgenero=2), 'A', 
                  'Lee', 'Lopez', 11111111,'leealeszan@gmail.com', False, False, random.choice(estados_usuario), 'img/usuario4.jpg', 
                  get_next_sequence_value(cursor, 'paciente_seq'),'','', '', '', '', '', '', '',bio)
    #PSICOLOGOS (13)
    crear_usuario(get_next_sequence_value(cursor, 'usuario_seq'), 'psico1', 'psicologo', Genero.objects.get(idgenero=2), 'Carolina', 
                  'Guerra', 'Morales', 11111111, 'cguerra@gmail.com', False, False, random.choice(estados_usuario), 'img/psico1.jpg', '',
                  get_next_sequence_value(cursor, 'psicologo_seq'), Rangoetario.objects.get(idrangoetario=2), random.choice(corrientes_psicologicas), 
                  random.choice(rangos_precio), random.choice(motivos_sesion), Coberturasalud.objects.get(idcoberturasalud=1), random.choice(diagnosticos), 
                  random.choice(tipos_sesion),bio)
    crear_usuario(get_next_sequence_value(cursor, 'usuario_seq'), 'psico2', 'psicologo', Genero.objects.get(idgenero=3), 'Daniela', 
                  'Lopez', 'Martinez', 11111111, 'dlopez@gmail.com', False, False, random.choice(estados_usuario), 'img/psico2.jpg', '',
                  get_next_sequence_value(cursor, 'psicologo_seq'), Rangoetario.objects.get(idrangoetario=4), random.choice(corrientes_psicologicas), 
                  random.choice(rangos_precio), random.choice(motivos_sesion), Coberturasalud.objects.get(idcoberturasalud=1), random.choice(diagnosticos), 
                  random.choice(tipos_sesion),bio)
    crear_usuario(get_next_sequence_value(cursor, 'usuario_seq'), 'psico3', 'psicologo', Genero.objects.get(idgenero=2), 'Lucia', 
                  'Martinez', 'Garcia', 11111111, 'lmartinez@gmail.com', False, False, random.choice(estados_usuario), 'img/psico3.jpg', '',
                  get_next_sequence_value(cursor, 'psicologo_seq'), Rangoetario.objects.get(idrangoetario=3), random.choice(corrientes_psicologicas), 
                  random.choice(rangos_precio), random.choice(motivos_sesion), Coberturasalud.objects.get(idcoberturasalud=2), random.choice(diagnosticos), 
                  random.choice(tipos_sesion),bio)
    crear_usuario(get_next_sequence_value(cursor, 'usuario_seq'), 'psico4', 'psicologo', Genero.objects.get(idgenero=3), 'Sofia', 
                  'Torres', 'Perez', 11111111,'storres@gmail.com', False, False, random.choice(estados_usuario), 'img/psico4.jpg', '',
                  get_next_sequence_value(cursor, 'psicologo_seq'), Rangoetario.objects.get(idrangoetario=3), random.choice(corrientes_psicologicas), 
                  random.choice(rangos_precio), random.choice(motivos_sesion), Coberturasalud.objects.get(idcoberturasalud=2), random.choice(diagnosticos), 
                  random.choice(tipos_sesion),bio)
    crear_usuario(get_next_sequence_value(cursor, 'usuario_seq'), 'psico5', 'psicologo', Genero.objects.get(idgenero=2), 'Maria', 
                  'Garcia', 'Lopez', 11111111,'mgarcia@gmail.com', False, False, random.choice(estados_usuario), 'img/psico5.jpg', '',
                  get_next_sequence_value(cursor, 'psicologo_seq'), Rangoetario.objects.get(idrangoetario=4), random.choice(corrientes_psicologicas), 
                  random.choice(rangos_precio), random.choice(motivos_sesion), Coberturasalud.objects.get(idcoberturasalud=4), random.choice(diagnosticos), 
                  random.choice(tipos_sesion),bio)
    crear_usuario(get_next_sequence_value(cursor, 'usuario_seq'), 'psico6', 'psicologo', Genero.objects.get(idgenero=2), 'Isabella', 
                  'Norambuena', 'Salas', 11111111, 'inorambuena@gmail.com', False, False, random.choice(estados_usuario), 'img/psico6.jpg', '',
                  get_next_sequence_value(cursor, 'psicologo_seq'), Rangoetario.objects.get(idrangoetario=2), random.choice(corrientes_psicologicas), 
                  random.choice(rangos_precio), random.choice(motivos_sesion), Coberturasalud.objects.get(idcoberturasalud=2), random.choice(diagnosticos), 
                  random.choice(tipos_sesion),bio)
    crear_usuario(get_next_sequence_value(cursor, 'usuario_seq'), 'psico7', 'psicologo', Genero.objects.get(idgenero=2), 'Ana', 
                  'Valenzuela', 'Gutierrez', 11111111, 'avalenzuela@gmail.com', False, False, random.choice(estados_usuario), 'img/psico7.jpg', '',
                  get_next_sequence_value(cursor, 'psicologo_seq'), Rangoetario.objects.get(idrangoetario=3), random.choice(corrientes_psicologicas), 
                  random.choice(rangos_precio), random.choice(motivos_sesion), Coberturasalud.objects.get(idcoberturasalud=2), random.choice(diagnosticos), 
                  random.choice(tipos_sesion),bio)
    crear_usuario(get_next_sequence_value(cursor, 'usuario_seq'), 'psico8', 'psicologo', Genero.objects.get(idgenero=1), 'Lucas', 
                  'Morales', 'Guerra', 11111111, 'lmorales@gmail.com', False, False, random.choice(estados_usuario), 'img/psico8.jpg', '',
                  get_next_sequence_value(cursor, 'psicologo_seq'), Rangoetario.objects.get(idrangoetario=2), random.choice(corrientes_psicologicas), 
                  random.choice(rangos_precio), random.choice(motivos_sesion), Coberturasalud.objects.get(idcoberturasalud=1), random.choice(diagnosticos), 
                  random.choice(tipos_sesion),bio)
    crear_usuario(get_next_sequence_value(cursor, 'usuario_seq'), 'psico9', 'psicologo', Genero.objects.get(idgenero=2), 'Marta', 
                  'Cáceres', 'Torres', 11111111,'mlcaceres@gmail.com', False, False, random.choice(estados_usuario), 'img/psico9.jpg', '',
                  get_next_sequence_value(cursor, 'psicologo_seq'), Rangoetario.objects.get(idrangoetario=2), random.choice(corrientes_psicologicas), 
                  random.choice(rangos_precio), random.choice(motivos_sesion), Coberturasalud.objects.get(idcoberturasalud=1), random.choice(diagnosticos), 
                  random.choice(tipos_sesion),bio)
    crear_usuario(get_next_sequence_value(cursor, 'usuario_seq'), 'psico10', 'psicologo', Genero.objects.get(idgenero=2), 'Andrea', 
                  'Rebolledo', 'Martinez', 11111111, 'arebolledo@gmail.com', False, False, random.choice(estados_usuario), 'img/psico10.jpg', '',
                  get_next_sequence_value(cursor, 'psicologo_seq'), Rangoetario.objects.get(idrangoetario=1), random.choice(corrientes_psicologicas), 
                  random.choice(rangos_precio), random.choice(motivos_sesion), Coberturasalud.objects.get(idcoberturasalud=1), random.choice(diagnosticos), 
                  random.choice(tipos_sesion),bio)
    crear_usuario(get_next_sequence_value(cursor, 'usuario_seq'), 'psico11', 'psicologo', Genero.objects.get(idgenero=2), 'Jacinta', 
                  'Zoro', 'Martinez', 11111111, 'ja.leppez@duocuc.cl', False, False, random.choice(estados_usuario), 'img/psico11.jpg', '',
                  get_next_sequence_value(cursor, 'psicologo_seq'), Rangoetario.objects.get(idrangoetario=1), random.choice(corrientes_psicologicas), 
                  random.choice(rangos_precio), random.choice(motivos_sesion), Coberturasalud.objects.get(idcoberturasalud=1), random.choice(diagnosticos), 
                  random.choice(tipos_sesion),bio)
    
    
    
    
    
    

#     agendas = [
#         Agenda(
#             idagenda=get_next_sequence_value(cursor, 'agenda_seq'),
#             notasadicionales=f"Notas adicionales {i}",
#             usuario_idusuario=random.choice(usuarios),
#         )
#         for i in range(5)
#     ]
#     Agenda.objects.bulk_create(agendas)

#     dias_disponibles = [
#         Diadisponible(
#             iddiadisponible=get_next_sequence_value(cursor, 'diadisponible_seq'),
#             fechahora=date.today() + timedelta(days=i),
#             agenda_idagenda=random.choice(agendas),
#         )
#         for i in range(5)
#     ]
#     Diadisponible.objects.bulk_create(dias_disponibles)

#     sesiones = []
#     for i in range(num_sessions):
#         idsesion = get_next_sequence_value(cursor, 'sesion_seq')
#         fechahora = date.today() + timedelta(days=random.randint(1, 30))
#         notas = f"Notas de la sesión {i}"
#         estadosesion = random.choice(estados_sesion)
#         tiposesion = random.choice(tipos_sesion)
#         usuario = random.choice(usuarios)

#         sesion = Sesion(
#             idsesion=idsesion, fechahora=fechahora, notas=notas, estadosesion_idestadosesion=estadosesion,
#             tiposesion_idtiposesion=tiposesion, usuario_idusuario=usuario
#         )
#         sesiones.append(sesion)

#     Sesion.objects.bulk_create(sesiones)

#     pagos = [
#         Pago(
#             idpago=get_next_sequence_value(cursor, 'pago_seq'),
#             fechahora=date.today(),
#             montototal=random.randint(20000, 80000),
#             sesion_idsesion=random.choice(sesiones),
#             metodopago_idmetodopago=random.choice(metodos_pago),
#         )
#         for _ in range(10)
#     ]
#     Pago.objects.bulk_create(pagos)

#     reseñas = [
#         Resena(
#             idresena=get_next_sequence_value(cursor, 'resena_seq'),
#             puntuacion=random.choice([True, False]),
#             comentarios=f"Comentarios de la reseña {i}",
#             sesion_idsesion=random.choice(sesiones),
#         )
#         for i in range(5)
#     ]
#     Resena.objects.bulk_create(reseñas)

#     mensajes = [
#         Mensaje(
#             idmensaje=get_next_sequence_value(cursor, 'mensaje_seq'),
#             fechahora=date.today() - timedelta(days=i),
#             contenido=f"Contenido del mensaje {i}",
#             usuario_idusuario=random.choice(usuarios),
#         )
#         for i in range(5)
#     ]
#     Mensaje.objects.bulk_create(mensajes)

#     notificaciones = [
#         Notificacion(
#             idnotificacion=get_next_sequence_value(cursor, 'notificacion_seq'),
#             fechahora=date.today(),
#             asunto=f"Asunto de la notificación {i}",
#             detalle=f"Detalle de la notificación {i}",
#             usuario_idusuario=random.choice(usuarios),
#         )
#         for i in range(5)
#     ]
#     Notificacion.objects.bulk_create(notificaciones)

#     tickets_soporte = [
#         Ticketsoporte(
#             idticketsoporte=get_next_sequence_value(cursor, 'ticketsoporte_seq'),
#             fechahora=date.today(),
#             contenido=f"Contenido del ticket de soporte {i}",
#             usuario_idusuario=random.choice(usuarios),
#         )
#         for i in range(5)
#     ]
#     Ticketsoporte.objects.bulk_create(tickets_soporte)
    
#    
            

#     #         # Create related records
#     #         if usuario.tipousuario == 'paciente':
#     #             Paciente.objects.create(pac_idusuario=usuario)

#     #             # Crear TestPaciente 
#     #             cursor.execute("SELECT test_seq.NEXTVAL FROM DUAL")
#     #             test_id = cursor.fetchone()[0]
#     #             test = Test.objects.create(
#     #                 idtest=test_id,
#     #                 generopsicologo_idgeneropsicologo=random.choice(generos_psicologo),
#     #                 rangoetario_idrangoetario=random.choice(rangos_etarios),
#     #                 corrientepsicologica_idcorrientepsicologica=random.choice(corrientes_psicologicas),
#     #                 rangoprecio_idrangoprecio=random.choice(rangos_precio),
#     #                 motivosesion_idmotivosesion=random.choice(motivos_sesion),
#     #                 coberturasalud_idcoberturasalud=random.choice(coberturas_salud),
#     #                 diagnostico_iddiagnostico=random.choice(diagnosticos),
#     #                 tiposesion_idtiposesion=random.choice(tipos_sesion),
#     #                 idusuariotest=usuario
#     #             )
#     #             Testpaciente.objects.create(
#     #                 idtest=test,
#     #                 generopsicologo_idgeneropsicologo=random.choice(generos_psicologo).idgeneropsicologo
#     #             )
#     #         else:
#     #             psicologo = Psicologo.objects.create(
#     #                 psi_idusuario=usuario,
#     #                 rangoetario_idrangoetario=random.choice(rangos_etarios),
#     #                 corrientepsicologica_idcorrientepsicologica=random.choice(corrientes_psicologicas),
#     #                 rangoprecio_idrangoprecio=random.choice(rangos_precio),
#     #                 motivosesion_idmotivosesion=random.choice(motivos_sesion),
#     #                 coberturasalud_idcoberturasalud=random.choice(coberturas_salud),
#     #                 diagnostico_iddiagnostico=random.choice(diagnosticos),
#     #                 tiposesion_idtiposesion=random.choice(tipos_sesion),
#     #                 numeroregistrolicencia=random.randint(1000000, 9999999)
#     #             )

#     #     except Exception as e:
#     #         print(f"Error creating user {i}: {e}")
#     #     # Crear Agenda para cada usuario
#     #     agenda = Agenda.objects.create(
#     #         usuario_idusuario=usuario,
#     #         notasadicionales=f'Notas adicionales para {user.username}'
#     #     )

#     #     # Crear algunos DiasDisponibles para cada Agenda
#     #     for _ in range(random.randint(1, 5)):
#     #         Diadisponible.objects.create(
#     #             fechahora=date.today() + timedelta(days=random.randint(1, 30)),
#     #             agenda_idagenda=agenda
#     #         )

#     # # superuser = User.objects.create_superuser('psicocare', 'psicocareduoc@gmail.com', 'psicocare1234') 

#     # # Crear sesiones ahora que existen pacientes y psicologos
#     # for i in range(num_sessions):
#     #     paciente = random.choice(Usuario.objects.filter(tipousuario='Paciente'))
#     #     psicologo = random.choice(Usuario.objects.filter(tipousuario='Psicologo'))
#     #     fecha_hora = date.today() + timedelta(days=random.randint(1, 30))
#     #     sesion = Sesion.objects.create(
#     #         fechahora=fecha_hora,
#     #         notas=f'Notas de la sesión {i}',
#     #         estadosesion_idestadosesion=random.choice(estados_sesion),
#     #         tiposesion_idtiposesion=random.choice(tipos_sesion),
#     #         usuario_idusuario=paciente
#     #     )

#     #     Pago.objects.create(
#     #         fechahora=fecha_hora,
#     #         montototal=random.randint(25000, 50000),
#     #         sesion_idsesion=sesion,
#     #         metodopago_idmetodopago=random.choice(metodos_pago)
#     #     )

#     #     Resena.objects.create(
#     #         puntuacion=random.choice([True, False]),
#     #         comentarios=f'Comentarios de la sesión {i}',
#     #         sesion_idsesion=sesion
#     #     )

#     #     Pacientepsicologo.objects.create(
#     #         psicologo_idusuario=psicologo.idusuario,
#     #         paciente_idusuario=paciente.idusuario
#     #     )

#     #     # Crear algunos Mensajes para cada Sesion
#     #     for _ in range(random.randint(1, 3)):
#     #         Mensaje.objects.create(
#     #             fechahora=fecha_hora,
#     #             contenido=f'Contenido del mensaje para la sesión {sesion.idsesion}',
#     #             usuario_idusuario=random.choice([paciente, psicologo])
#     #         )

#     # # Crear algunos TicketsSoporte
#     # for i in range(random.randint(1, 10)):
#     #     Ticketsoporte.objects.create(
#     #         fechahora=date.today(),
#     #         contenido=f'Contenido del ticket de soporte {i}',
#     #         usuario_idusuario=random.choice(users)
#     #     )

#     # # Crear algunos Administradores
#     # for _ in range(random.randint(1, 3)):
#     #     Administrador.objects.create(
#     #         adm_idusuario=random.choice(users)
#     #     )

#     # # Crear algunas Notificaciones
#     # for i in range(random.randint(1, 20)):
#     #     Notificacion.objects.create(
#     #         fechahora=date.today(),
#     #         asunto=f'Asunto de la notificación {i}',
#     #         detalle=f'Detalle de la notificación {i}',
#     #         usuario_idusuario=random.choice(users)
#     #     )


if __name__ == '__main__':
    populate_database()
