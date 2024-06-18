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

    def __str__(self):
        return f'{self.author.username} - {self.timestamp}'

# from typing import List, Dict
# from collections import defaultdict

# # ... (Your existing model imports and definitions)

# def find_compatible_psychologists(patient_test: Test) -> List[Psicologo]:
#     """
#     Finds compatible psychologists for a given patient based on their test answers.

#     Args:
#         patient_test: The Test object representing the patient's answers.

#     Returns:
#         A list of Psicologo objects representing the compatible psychologists.
#     """

#     # 1. Define matching criteria and their weights
#     matching_criteria = {
#         "generopsicologo_idgeneropsicologo": 3,
#         "rangoetario_idrangoetario": 2,
#         "corrientepsicologica_idcorrientepsicologica": 5,
#         "rangoprecio_idrangoprecio": 4,
#         "motivosesion_idmotivosesion": 4,
#         "coberturasalud_idcoberturasalud": 3,
#         "diagnostico_iddiagnostico": 5,
#         "tiposesion_idtiposesion": 2,
#     }

#     # 2. Fetch all psychologists
#     all_psychologists = Psicologo.objects.all()

#     # 3. Calculate compatibility scores
#     compatibility_scores = defaultdict(int)
#     for psychologist in all_psychologists:
#         for criterion, weight in matching_criteria.items():
#             # Get the values for comparison from the models
#             patient_value = getattr(patient_test, criterion)
#             psychologist_value = getattr(psychologist, criterion, None)  

#             # Handle cases where the psychologist might not have a value for a criterion
#             if psychologist_value is not None and patient_value == psychologist_value:
#                 compatibility_scores[psychologist.psi_idusuario_id] += weight

#     # 4. Sort psychologists by compatibility score (descending)
#     sorted_psychologists = sorted(
#         compatibility_scores.items(), key=lambda item: item[1], reverse=True
#     )

#     # 5. Return top 5 most compatible psychologists as Psicologo objects
#     top_psychologist_ids = [psychologist_id for psychologist_id, _ in sorted_psychologists[:5]]
#     return Psicologo.objects.filter(psi_idusuario_id__in=top_psychologist_ids)

# VIEWS 
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from .models import Test, Psicologo, Paciente, TestPaciente  # Import your models
# from .matching_logic import find_compatible_psychologists  # Assuming you put the matching logic in a file named matching_logic.py

# # ... other imports ...

# @login_required
# def take_test(request):
#     """View for a patient to take the test."""
#     if request.method == 'POST':
#         # Process the form data, create a TestPaciente instance
#         # ... (form handling logic) ...

#         test = Test.objects.create(
#             # ... (save data from the form to the Test model) ...
#         )
#         test_paciente = TestPaciente.objects.create(
#             idtest=test,
#             # ... (save additional data specific to TestPaciente) ...
#         )
#         return redirect('show_matches')  # Redirect to the results page
#     else:
#         # Render the test form
#         return render(request, 'take_test.html')

# @login_required
# def show_matches(request):
#     """View to display compatible psychologists to the patient."""
#     try:
#         patient_test = TestPaciente.objects.get(idusuariotest=request.user.id)
#     except TestPaciente.DoesNotExist:
#         return redirect('take_test')  # Redirect if the patient hasn't taken the test

#     compatible_psychologists = find_compatible_psychologists(patient_test.idtest)
    
#     return render(request, 'show_matches.html', {'psychologists': compatible_psychologists})

# # ... other views ...

# HTML

# {% extends 'base.html' %}
# {% block content %}
#     <h2>Your Compatible Psychologists</h2>
#     <ul>
#         {% for psychologist in psychologists %}
#             <li>
#                 <h3>{{ psychologist.psi_idusuario.user.first_name }} {{ psychologist.psi_idusuario.user.last_name }}</h3>
#                 <!-- Display other relevant psychologist information -->
#             </li>
#         {% endfor %}
#     </ul>
# {% endblock %}

