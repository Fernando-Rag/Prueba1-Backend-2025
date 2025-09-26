from django.db import models
from django.core.exceptions import ValidationError
from .validators import validate_rut_chile, normalize_rut, format_rut

class Visitante(models.Model):
    nombre_s = models.CharField(max_length=50)
    apellido_s = models.CharField(max_length=50)
    #para el rut ocupare charfield para los ruts que terminan el y validate_rut_chile para validar el rut con el algoritmo de modulo 11
    rut = models.CharField("RUT", max_length=12, unique=True, validators=[validate_rut_chile])
    #esta el la funcion para que el rur validado se ingrese en un formato estandar en la base de datos
    def limpiador(self):
        super().clean()
        try:
            #separa los digitos del digito verificador
            numero, dv = normalize_rut(self.rut)
            # normalize_rut formato 12.345.678-5
            self.rut = format_rut(numero, dv)
        except ValidationError as e:
            raise e

    def __str__(self):
        return f"{self.nombre_s} {self.apellido_s} ({self.rut})"
    motivo_visita = models.CharField(max_length=100)
    hora_entrada = models.
    hora_salida = models.
