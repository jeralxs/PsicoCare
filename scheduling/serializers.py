from rest_framework import serializers
from django.utils import timezone
from datetime import datetime

class DateTimeFieldSerializer(serializers.Field):
    def to_representation(self, value):
        if isinstance(value, str):
            # Si el valor es una cadena, intenta convertirlo a datetime
            try:
                value = datetime.fromisoformat(value)
            except ValueError:
                # Si no se puede convertir, devuelve el valor original
                return value
        return timezone.localtime(value).isoformat()

    def to_internal_value(self, data):
        return timezone.parse_datetime(data)