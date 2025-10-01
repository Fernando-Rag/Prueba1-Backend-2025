from django import forms
from .models import Visitante, RegistroEntrada, RegistroSalida

class VisitanteForm(forms.ModelForm):
    class Meta:
        model = Visitante
        fields = ["nombre_s", "apellido_s", "edad", "rut"]

class RegistroEntradaForm(forms.ModelForm):
    class Meta:
        model = RegistroEntrada
        fields = ["visitante", "motivo"]

class RegistroSalidaForm(forms.ModelForm):
    class Meta:
        model = RegistroSalida
        fields = ["visitante"]