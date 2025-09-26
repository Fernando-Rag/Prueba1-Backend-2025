from django.db import models

class Visitante(models.Model):
    nombre_s = models.CharField(max_length=50)
    apellido_s = models.CharField(max_length=50)
    rut = models.DecimalField(max_digits=9)
    