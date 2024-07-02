from django.db import models
from django.contrib.auth.models import User
from collections import defaultdict

class Administrador(models.Model):
    adm_idusuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='adm_idusuario')

    class Meta:
        managed = False
        db_table = 'administrador'


class Agenda(models.Model):
    idagenda = models.AutoField(primary_key=True)
    notasadicionales = models.CharField(max_length=512)
    usuario_idusuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuario_idusuario')

    class Meta:
        managed = False
        db_table = 'agenda'



class Coberturasalud(models.Model):
    idcoberturasalud = models.AutoField(primary_key=True)
    coberturasalud = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'coberturasalud'
    def __str__(self):
        return u'{0}'.format(self.coberturasalud)


class Corrientepsicologica(models.Model):
    idcorrientepsicologica = models.AutoField(primary_key=True)
    corrientepsicologica = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'corrientepsicologica'
    def __str__(self):
        return u'{0}'.format(self.corrientepsicologica)


class Diadisponible(models.Model):
    iddiadisponible = models.AutoField(primary_key=True)
    fechahora = models.DateField()
    agenda_idagenda = models.ForeignKey(Agenda, models.DO_NOTHING, db_column='agenda_idagenda')

    class Meta:
        managed = False
        db_table = 'diadisponible'


class Diagnostico(models.Model):
    iddiagnostico = models.AutoField(primary_key=True)
    diagnostico = models.CharField(max_length=64)
    descripcion = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'diagnostico'
    def __str__(self):
        return u'{0}'.format(self.diagnostico)


class Estadosesion(models.Model):
    idestadosesion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'estadosesion'


class Estadousuario(models.Model):
    idestadousuario = models.AutoField(primary_key=True)
    estadousuario = models.CharField(max_length=64, blank=True, null=True)
    descripcion = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'estadousuario'

class Genero(models.Model):
    idgenero = models.AutoField(primary_key=True)
    n_genero = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'genero'

class Generopsicologo(models.Model):
    idgeneropsicologo = models.AutoField(primary_key=True)
    genero = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'generopsicologo'
    def __str__(self):
        return u'{0}'.format(self.genero)


class Mensaje(models.Model):
    idmensaje = models.AutoField(primary_key=True)
    fechahora = models.DateField()
    contenido = models.CharField(max_length=512)
    usuario_idusuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuario_idusuario')

    class Meta:
        managed = False
        db_table = 'mensaje'


class Metodopago(models.Model):
    idmetodopago = models.AutoField(primary_key=True)
    metodopago = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=128)
    habilitado = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'metodopago'


class Motivosesion(models.Model):
    idmotivosesion = models.AutoField(primary_key=True)
    motivosesion = models.CharField(max_length=64)
    descripcion = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'motivosesion'
    def __str__(self):
        return u'{0}'.format(self.motivosesion)


class Notificacion(models.Model):
    idnotificacion = models.AutoField(primary_key=True)
    fechahora = models.DateField()
    asunto = models.CharField(max_length=128)
    detalle = models.CharField(max_length=256, blank=True, null=True)
    usuario_idusuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuario_idusuario')

    class Meta:
        managed = False
        db_table = 'notificacion'





class Pacientepsicologo(models.Model):
    idpacpsico = models.AutoField(primary_key=True)
    psicologo_idusuario = models.ForeignKey('Psicologo', models.DO_NOTHING, db_column='psicologo_idusuario')
    paciente_idusuario = models.ForeignKey('Paciente', models.DO_NOTHING, db_column='paciente_idusuario')

    class Meta:
        managed = False
        db_table = 'pacientepsicologo'


class Pago(models.Model):
    idpago = models.AutoField(primary_key=True)
    fechahora = models.DateField()
    montototal = models.IntegerField()
    sesion_idsesion = models.ForeignKey('Sesion', models.DO_NOTHING, db_column='sesion_idsesion')
    metodopago_idmetodopago = models.ForeignKey(Metodopago, models.DO_NOTHING, db_column='metodopago_idmetodopago')

    class Meta:
        managed = False
        db_table = 'pago'



class Rangoetario(models.Model):
    idrangoetario = models.AutoField(primary_key=True)
    rangoetario = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'rangoetario'
    def __str__(self):
        return u'{0}'.format(self.rangoetario)


class Rangoprecio(models.Model):
    idrangoprecio = models.AutoField(primary_key=True)
    montominimo = models.IntegerField()
    montomaximo = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'rangoprecio'
    def __str__(self):
        return u'{0}'.format( f'{self.montominimo} - {self.montomaximo}')


class Resena(models.Model):
    idresena = models.AutoField(primary_key=True)
    puntuacion = models.BooleanField()
    comentarios = models.CharField(max_length=512)
    sesion_idsesion = models.ForeignKey('Sesion', models.DO_NOTHING, db_column='sesion_idsesion')

    class Meta:
        managed = False
        db_table = 'resena'


class Sesion(models.Model):
    idsesion = models.AutoField(primary_key=True)
    fechahora = models.DateField()
    notas = models.CharField(max_length=1024, blank=True, null=True)
    estadosesion_idestadosesion = models.ForeignKey(Estadosesion, models.DO_NOTHING, db_column='estadosesion_idestadosesion')
    tiposesion_idtiposesion = models.ForeignKey('Tiposesion', models.DO_NOTHING, db_column='tiposesion_idtiposesion')
    usuario_idusuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuario_idusuario')

    class Meta:
        managed = False
        db_table = 'sesion'


class Superusuario(models.Model):
    sup_idusuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='sup_idusuario')

    class Meta:
        managed = False
        db_table = 'superusuario'


class Test(models.Model):
    idtest = models.AutoField(primary_key=True)
    generopsicologo_idgenero = models.ForeignKey(Generopsicologo, models.DO_NOTHING, db_column='generopsicologo_idgenero')
    rangoetario_idrangoetario = models.ForeignKey(Rangoetario, models.DO_NOTHING, db_column='rangoetario_idrangoetario')
    corriente_idcorriente = models.ForeignKey(Corrientepsicologica, models.DO_NOTHING, db_column='corriente_idcorriente')
    rangoprecio_idrangoprecio = models.ForeignKey(Rangoprecio, models.DO_NOTHING, db_column='rangoprecio_idrangoprecio')
    motivosesion_idmotivosesion = models.ForeignKey(Motivosesion, models.DO_NOTHING, db_column='motivosesion_idmotivosesion')
    coberturasalud_idcobertura  = models.ForeignKey(Coberturasalud, models.DO_NOTHING, db_column='coberturasalud_idcobertura')
    diagnostico_iddiagnostico = models.ForeignKey(Diagnostico, models.DO_NOTHING, db_column='diagnostico_iddiagnostico')
    tiposesion_idtiposesion = models.ForeignKey('Tiposesion', models.DO_NOTHING, db_column='tiposesion_idtiposesion')
    idusuariotest = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='idusuariotest')

    class Meta:
        managed = False
        db_table = 'test'


class Testpaciente(models.Model):
    idtest = models.OneToOneField(Test, models.DO_NOTHING, db_column='idtest', primary_key=True)
    generopsicologo_idgeneropsicologo = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'testpaciente'


class Testpsicologo(models.Model):
    idtest = models.OneToOneField(Test, models.DO_NOTHING, db_column='idtest', primary_key=True)
    rangoetario_idrangoetario = models.ForeignKey(Rangoetario, models.DO_NOTHING, db_column='rangoetario_idrangoetario')

    class Meta:
        managed = False
        db_table = 'testpsicologo'


class Ticketsoporte(models.Model):
    idticketsoporte = models.AutoField(primary_key=True)
    fechahora = models.DateField()
    contenido = models.CharField(max_length=512)
    usuario_idusuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuario_idusuario')

    class Meta:
        managed = False
        db_table = 'ticketsoporte'


class Tiposesion(models.Model):
    idtiposesion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=64)
    descripcion = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tiposesion'
    def __str__(self):
        return u'{0}'.format(self.nombre)


class Usuario(models.Model):
    idusuario = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, models.DO_NOTHING)
    genero_idgenero = models.ForeignKey(Genero, models.DO_NOTHING, db_column='genero_idgenero')
    foto = models.CharField(max_length=200, blank=True, null=True)
    apellido_materno = models.CharField(max_length=64, blank=True, null=True)
    telefono = models.CharField(max_length=64)
    estadousuario_idestadousuario = models.ForeignKey(Estadousuario, models.DO_NOTHING, db_column='estadousuario_idestadousuario')
    tipousuario = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'usuario'

class Psicologo(models.Model):
    idpsicologo = models.AutoField(primary_key=True)
    bio_info = models.CharField(max_length=512)
    psi_idusuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='psi_idusuario')
    rangoetario_idrangoetario = models.ForeignKey(Rangoetario, models.DO_NOTHING, db_column='rangoetario_idrangoetario')
    corriente_idcorriente = models.ForeignKey(Corrientepsicologica, models.DO_NOTHING, db_column='corriente_idcorriente')
    rangoprecio_idrangoprecio = models.ForeignKey(Rangoprecio, models.DO_NOTHING, db_column='rangoprecio_idrangoprecio')
    motivosesion_idmotivosesion = models.ForeignKey(Motivosesion, models.DO_NOTHING, db_column='motivosesion_idmotivosesion')
    coberturasalud_id = models.ForeignKey(Coberturasalud, models.DO_NOTHING, db_column='coberturasalud_id')
    diagnostico_iddiagnostico = models.ForeignKey(Diagnostico, models.DO_NOTHING, db_column='diagnostico_iddiagnostico')
    tiposesion_idtiposesion = models.ForeignKey('Tiposesion', models.DO_NOTHING, db_column='tiposesion_idtiposesion')
    numeroregistrolicencia = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'psicologo'

class Paciente(models.Model):
    idpaciente = models.AutoField(primary_key=True)
    pac_idusuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='pac_idusuario')

    class Meta:
        managed = False
        db_table = 'paciente'


class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')

class Mensaje(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='mensajes')
    author = models.ForeignKey(User, models.DO_NOTHING, db_column='author')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username} - {self.timestamp}'


def puntaje_match(psicologo, test):
    score = 0
    print(f"Evaluando psicólogo: {psicologo.idpsicologo}")

    if psicologo.psi_idusuario.genero_idgenero is not None and test.generopsicologo_idgenero  is not None:
        print(f"Comparando corriente: {psicologo.psi_idusuario.genero_idgenero} vs {test.generopsicologo_idgenero}")
        if test.generopsicologo_idgenero == 4:
            score += 0
        else:
            if psicologo.psi_idusuario.genero_idgenero == test.generopsicologo_idgenero:
                score += 2

    if psicologo.corriente_idcorriente is not None and test.corriente_idcorriente is not None:
        print(f"Comparando corriente: {psicologo.corriente_idcorriente} vs {test.corriente_idcorriente}")
        if psicologo.corriente_idcorriente == test.corriente_idcorriente:
            score += 2

    if psicologo.rangoetario_idrangoetario is not None and test.rangoetario_idrangoetario is not None:
        print(f"Comparando rango etario: {psicologo.rangoetario_idrangoetario} vs {test.rangoetario_idrangoetario}")
        if psicologo.rangoetario_idrangoetario == test.rangoetario_idrangoetario:
            score += 3

    if psicologo.motivosesion_idmotivosesion is not None and test.motivosesion_idmotivosesion is not None:
        print(f"Comparando motivo sesión: {psicologo.motivosesion_idmotivosesion} vs {test.motivosesion_idmotivosesion}")
        if psicologo.motivosesion_idmotivosesion == test.motivosesion_idmotivosesion:
            score += 2

    if psicologo.diagnostico_iddiagnostico is not None and test.diagnostico_iddiagnostico is not None:
        print(f"Comparando diagnóstico: {psicologo.diagnostico_iddiagnostico} vs {test.diagnostico_iddiagnostico}")
        if psicologo.diagnostico_iddiagnostico == test.diagnostico_iddiagnostico:
            score += 2

    if psicologo.rangoprecio_idrangoprecio is not None and test.rangoprecio_idrangoprecio is not None:
        print(f"Comparando rango de precio: {psicologo.rangoprecio_idrangoprecio} vs {test.rangoprecio_idrangoprecio}")
        if psicologo.rangoprecio_idrangoprecio == test.rangoprecio_idrangoprecio:
            score += 2

    if psicologo.tiposesion_idtiposesion is not None and test.tiposesion_idtiposesion is not None:
        print(f"Comparando tipo de sesión: {psicologo.tiposesion_idtiposesion} vs {test.tiposesion_idtiposesion}")
        if psicologo.tiposesion_idtiposesion == test.tiposesion_idtiposesion:
            score += 2

    if psicologo.coberturasalud_id is not None and test.coberturasalud_idcobertura is not None:
        print(f"Comparando cobertura de salud: {psicologo.coberturasalud_id} vs {test.coberturasalud_idcobertura}")
        if psicologo.coberturasalud_id == test.coberturasalud_idcobertura:
            score += 2

    print(f"Score final para psicólogo {psicologo.idpsicologo}: {score}")
    return score

# class Schedule(models.Model):
#     schedule_id = models.AutoField(primary_key=True) 
#     psicologo = models.ForeignKey(Psicologo, on_delete=models.CASCADE)
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField()
#     available = models.BooleanField(default=True)

# class Appointment(models.Model):
#     paciente = models.ForeignKey(Paciente, models.DO_NOTHING, db_column="paciente")
#     psicologo = models.ForeignKey(Psicologo, models.DO_NOTHING, db_column="psicologo")
#     schedule = models.ForeignKey(Schedule, models.DO_NOTHING, db_column="schedule")
#     confirmed = models.BooleanField(default=False)