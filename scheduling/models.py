

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from core.models import Psicologo, Paciente


class Schedule(models.Model):
    schedule_id = models.AutoField(primary_key=True) 
    psicologo = models.ForeignKey(Psicologo, models.DO_NOTHING, db_column="psicologo")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    valor = models.IntegerField()
    available = models.BooleanField(default=True)
    link_h = models.CharField(max_length=1)
    class Meta:
        managed = False
        db_table = 'schedule'

class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True) 
    paciente = models.ForeignKey(Paciente, models.DO_NOTHING, db_column="paciente")
    psicologo = models.ForeignKey(Psicologo, models.DO_NOTHING, db_column="psicologo")
    schedule = models.ForeignKey(Schedule, models.DO_NOTHING, db_column="schedule")
    confirmed = models.BooleanField(default=False)
    class Meta:
        managed = False
        db_table = 'appointment'

