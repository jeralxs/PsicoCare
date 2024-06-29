from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Schedule(models.Model):
    psychologist = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    available = models.BooleanField(default=True)

class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_appointments')
    psychologist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='psychologist_appointments')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)

