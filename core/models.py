from django.db import models
from django.contrib.auth.models import User

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


class Corrientepsicologica(models.Model):
    idcorrientepsicologica = models.AutoField(primary_key=True)
    corrientepsicologica = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'corrientepsicologica'


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
    psicologo_idusuario = models.IntegerField(primary_key=True)  # The composite primary key (psicologo_idusuario, paciente_idusuario) found, that is not supported. The first column is selected.
    paciente_idusuario = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pacientepsicologo'
        unique_together = (('psicologo_idusuario', 'paciente_idusuario'),)


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


class Rangoprecio(models.Model):
    idrangoprecio = models.AutoField(primary_key=True)
    montominimo = models.IntegerField()
    montomaximo = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'rangoprecio'


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
    generopsicologo_idgeneropsicologo = models.ForeignKey(Generopsicologo, models.DO_NOTHING, db_column='generopsicologo_idgeneropsicologo')
    rangoetario_idrangoetario = models.ForeignKey(Rangoetario, models.DO_NOTHING, db_column='rangoetario_idrangoetario')
    corriente_idcorriente = models.ForeignKey(Corrientepsicologica, models.DO_NOTHING, db_column='corriente_idcorriente')
    rangoprecio_idrangoprecio = models.ForeignKey(Rangoprecio, models.DO_NOTHING, db_column='rangoprecio_idrangoprecio')
    motivosesion_idmotivosesion = models.ForeignKey(Motivosesion, models.DO_NOTHING, db_column='motivosesion_idmotivosesion')
    coberturasalud_id  = models.ForeignKey(Coberturasalud, models.DO_NOTHING, db_column='coberturasalud_id ')
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
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f'{self.author.username} - {self.timestamp}'












