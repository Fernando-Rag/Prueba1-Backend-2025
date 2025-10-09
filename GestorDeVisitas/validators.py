import re
import itertools
from django.core.exceptions import ValidationError

#este archivo tiene como funcion principal validar el rut 
#lo exporte de forma sensilla ya que esta es una formula matematica conocida para validar un rur en chile 
#llamada modulo 11

RUT_CLEAN_RE = re.compile(r"[^0-9Kk]")

def normalize_rut(value: str):
    if value is None:
        raise ValidationError("RUT requerido.")
    s = str(value).strip().upper()
    s = RUT_CLEAN_RE.sub("", s)
    if len(s) < 2:
        raise ValidationError("RUT muy corto.")
    numero, dv = s[:-1], s[-1]
    if not numero.isdigit():
        raise ValidationError("La parte numérica contiene caracteres inválidos.")
    if dv not in "0123456789K":
        raise ValidationError("Dígito verificador inválido.")
    if not (1 <= len(numero) <= 8):
        raise ValidationError("La parte numérica debe tener entre 1 y 8 dígitos.")
    return numero, dv

def _compute_rut_dv(numero: str) -> str:
    factores = itertools.cycle([2, 3, 4, 5, 6, 7])
    total = sum(int(d) * next(factores) for d in reversed(numero))
    resto = 11 - (total % 11)
    if resto == 11:
        return "0"
    if resto == 10:
        return "K"
    return str(resto)

def format_rut(numero: str, dv: str) -> str:
    partes = f"{int(numero):,}".replace(",", ".")
    return f"{partes}-{dv}"

def validate_rut_chile(value: str):
    numero, dv = normalize_rut(value)
    esperado = _compute_rut_dv(numero)
    if dv != esperado:
        raise ValidationError("Ese rut no existe")