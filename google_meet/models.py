

# Create your models here.
from django.db import models
from core.models import Psicologo, Paciente
from scheduling.models import Schedule

class Sesion(models.Model):
    idsesion = models.AutoField(primary_key=True)
    schedule = models.ForeignKey(Schedule, models.DO_NOTHING, db_column="schedule")
    notas = models.CharField(max_length=512)
    paciente = models.ForeignKey(Paciente, models.DO_NOTHING, db_column="paciente")
    psicologo = models.ForeignKey(Psicologo, models.DO_NOTHING, db_column="psicologo")
    meeting_uri = models.URLField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    class Meta:
        managed = False
        db_table = 'sesion'