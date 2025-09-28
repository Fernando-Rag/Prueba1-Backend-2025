from django.http import HttpResponse
from django.shortcuts import render
from .models import Visitante, RegistroEntrada, RegistroSalida

def registroVisitante(request):
    return render(request, 'visitantes/registroVisitantes.html')

def registroEntrada(request):
    return render(request, 'visitantes/registroEntrada.html')

def registroSalida(request):
    return render(request, 'visitantes/registroSalida.html')

def busquedaVisitantes(request):
    return render(request, 'visitantes/busquedaVisitantes.html')