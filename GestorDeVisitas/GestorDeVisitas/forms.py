from django import forms
from .models import Visitante, RegistroEntrada, RegistroSalida

class VisitanteForm(forms.ModelForm):
    class Meta:
        model = Visitante
        fields = ["nombre_s", "apellido_s", "edad", "rut"]
        labels = {
            'nombre_s': 'Nombre/s',
            'apellido_s': 'Apellido/s',
            'edad': 'Edad',
            'rut': 'RUT',
        }
    
    def clean_nombre_s(self):
        nombre = self.cleaned_data['nombre_s'].strip()
        # Capitalizar cada palabra
        nombre = ' '.join([w.capitalize() for w in nombre.split()])
        # Validar que no haya números
        if not all(w.isalpha() for w in nombre.replace(' ', '')):
            raise forms.ValidationError("En esta casilla no pueden ir numeros")
        return nombre

    def clean_apellido_s(self):
        apellido = self.cleaned_data['apellido_s'].strip()
        apellido = ' '.join([w.capitalize() for w in apellido.split()])
        if not all(w.isalpha() for w in apellido.replace(' ', '')):
            raise forms.ValidationError("En esta casilla no puden ir numeros")
        return apellido

class RegistroEntradaForm(forms.ModelForm):
    class Meta:
        model = RegistroEntrada
        fields = ['visitante', 'motivo']
        widgets = {
            'visitante': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-black rounded focus:outline-none focus:ring-2 focus:ring-yellow-400'}),
            'motivo': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-black rounded focus:outline-none focus:ring-2 focus:ring-yellow-400'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo visitantes sin visita activa
        self.fields['visitante'].queryset = Visitante.objects.filter(visita_activa=False)

class RegistroSalidaForm(forms.ModelForm):
    class Meta:
        model = RegistroSalida
        fields = ['visitante']
        widgets = {
            'visitante': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-black rounded focus:outline-none focus:ring-2 focus:ring-yellow-400'
            }),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo visitantes con visita activa
        self.fields['visitante'].queryset = Visitante.objects.filter(visita_activa=True)