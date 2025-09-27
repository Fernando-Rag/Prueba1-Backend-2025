from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import Q, UniqueConstraint, F
from .validators import validate_rut_chile, normalize_rut, format_rut

class Visitante(models.Model):
    nombre_s = models.CharField(max_length=50)
    apellido_s = models.CharField(max_length=50)
    edad = models.IntegerField()
    rut = models.CharField("RUT", max_length=12, unique=True, db_index=True, validators=[validate_rut_chile])
    visita_activa = models.BooleanField(default=False)

    def clean(self):
        super().clean()
        try:
            numero, dv = normalize_rut(self.rut)
            self.rut = format_rut(numero, dv)
        except ValidationError as e:
            raise e

    def __str__(self):
        return f"{self.nombre_s} {self.apellido_s} ({self.rut})"


class RegistroEntrada(models.Model):
    visitante = models.ForeignKey(Visitante, on_delete=models.PROTECT, related_name="visitas")
    motivo = models.CharField(max_length=100)
    hora_entrada = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # solo permite crear registro si no hay visita activa
        if self.visitante.visita_activa:
            raise ValidationError("El visitante ya tiene una visita activa.")
        super().save(*args, **kwargs)
        # marca la visita como activa
        self.visitante.visita_activa = True
        self.visitante.save(update_fields=["visita_activa"])

    def __str__(self):
        return f"Entrada: {self.visitante} ({self.hora_entrada})"


class RegistroSalida(models.Model):
    visitante = models.ForeignKey(Visitante, on_delete=models.PROTECT, related_name="salidas")
    hora_salida = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # solo permite crear registro si hay visita activa
        if not self.visitante.visita_activa:
            raise ValidationError("El visitante no tiene una visita activa.")
        super().save(*args, **kwargs)
        # marca la visita como NO activa
        self.visitante.visita_activa = False
        self.visitante.save(update_fields=["visita_activa"])

    def __str__(self):
        return f"Salida: {self.visitante} ({self.hora_salida})"