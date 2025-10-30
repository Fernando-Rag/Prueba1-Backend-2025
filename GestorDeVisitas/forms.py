from django import forms
from .models import Visitante, RegistroEntrada, RegistroSalida

#creacion de formulario usando fomrs de django
class VisitanteForm(forms.ModelForm):
    class Meta:
        model = Visitante
        fields = ["nombre_s", "apellido_s", "edad", "rut"]
        # lo uso para que el titulo de la casilla tenga Nombre/s y no salga como nombre s
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
    
    def clean_edad(self):
       
        raw = self.cleaned_data.get('edad')

        # Si el campo viene ya como int desde el widget (IntegerField en el modelo)
        if isinstance(raw, int):
            valor = raw
        else:
            # Si viene como string (p. ej. por algún widget personalizado), validamos la cadena.
            if raw is None:
                raise forms.ValidationError("Edad es requerido.")
            # Normalizar espacios
            s = str(raw).strip()

            # No permitir comas ni puntos (decimales)
            if ',' in s or '.' in s:
                raise forms.ValidationError("Ingrese un número entero sin comas ni puntos.")

            # Solo dígitos (no signos + ni -)
            if not s.isdigit():
                raise forms.ValidationError("Ingrese solo dígitos (números enteros, sin signos ni letras).")

            # Máximo 3 dígitos
            if len(s) > 3:
                raise forms.ValidationError("La edad no puede tener más de 3 dígitos (máximo 999).")

            try:
                valor = int(s)
            except ValueError:
                raise forms.ValidationError("Valor de edad inválido.")

        # Rango 1..999 (no negativos)
        if valor < 1:
            raise forms.ValidationError("NO existe la edad negativa")
        if valor > 999:
            raise forms.ValidationError("Esa edad no es correcta")

        return valor


#creacion de formulario usando el forms de djago 
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
        #esto es para que me muestro solo a los visintes sin una visita activa
        self.fields['visitante'].queryset = Visitante.objects.filter(visita_activa=False)

#registro de salida con forms de django
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
        # esta parte hace que solo me muestre a los visitantes con una vista activa
        self.fields['visitante'].queryset = Visitante.objects.filter(visita_activa=True)