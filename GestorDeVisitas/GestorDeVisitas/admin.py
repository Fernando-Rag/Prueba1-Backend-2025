from django.contrib import admin
from .models import Visitante, RegistroEntrada, RegistroSalida

admin.site.register(Visitante)
admin.site.register(RegistroEntrada)
admin.site.register(RegistroSalida)