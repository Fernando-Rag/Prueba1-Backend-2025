from django.shortcuts import render, get_object_or_404, redirect
from .models import Visitante, RegistroEntrada, RegistroSalida
from .forms import VisitanteForm, RegistroEntradaForm, RegistroSalidaForm
from django.utils import timezone

# Visitante CRUD
def registroVisitante(request):
    visitantes = Visitante.objects.all()
    if request.method == 'POST':
        form = VisitanteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registroVisitante')
    else:
        form = VisitanteForm()
    return render(request, 'visitantes/registroVisitante.html', {'visitantes': visitantes, 'form': form})

def visitante_update(request, pk):
    visitante = get_object_or_404(Visitante, pk=pk)
    if request.method == 'POST':
        form = VisitanteForm(request.POST, instance=visitante)
        if form.is_valid():
            form.save()
            return redirect('registroVisitante')
    else:
        form = VisitanteForm(instance=visitante)
    return render(request, 'visitantes/registroVisitante.html', {'form': form, 'visitante': visitante})

def visitante_delete(request, pk):
    visitante = get_object_or_404(Visitante, pk=pk)
    if request.method == 'POST':
        visitante.delete()
        return redirect('registroVisitante')
    return render(request, 'visitantes/registroVisitante.html', {'visitante': visitante})

# Registro Entrada
def registroEntrada(request):
    error = None
    if request.method == 'POST':
        form = RegistroEntradaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('registroEntrada')
            except Exception as e:
                error = str(e)
    else:
        form = RegistroEntradaForm()

    # Solo la última entrada (visita activa) por visitante
    visitantes_activos = Visitante.objects.filter(visita_activa=True)
    entradas = []
    for v in visitantes_activos:
        ultima_entrada = v.visitas.order_by('-hora_entrada').first()
        if ultima_entrada:
            entradas.append(ultima_entrada)

    return render(request, 'visitantes/registroEntrada.html', {
        'entradas': entradas,
        'form': form,
        'error': error
    })


def registroSalida(request):
    error = None
    if request.method == 'POST':
        form = RegistroSalidaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('registroSalida')
            except Exception as e:
                error = str(e)
    else:
        form = RegistroSalidaForm()

    # Solo la última entrada (visita activa) por visitante
    visitantes_activos = Visitante.objects.filter(visita_activa=True)
    entradas = []
    for v in visitantes_activos:
        ultima_entrada = v.visitas.order_by('-hora_entrada').first()
        if ultima_entrada:
            entradas.append(ultima_entrada)

    return render(request, 'visitantes/registroSalida.html', {
        'entradas': entradas,
        'form': form,
        'error': error
    })

# Búsqueda de visitantes
def busquedaVisitantes(request):
    visitas = []
    rut = request.GET.get('rut', '').strip()
    rut_formateado = formatea_rut(rut) if rut else ''
    dia = request.GET.get('dia', '').strip()
    error = None

    if rut:
        try:
            visitante = Visitante.objects.get(rut=rut_formateado)
            entradas = RegistroEntrada.objects.filter(visitante=visitante).order_by('-hora_entrada')
        except Visitante.DoesNotExist:
            error = "No existe un visitante con ese RUT."
            entradas = []
    elif dia:
        try:
            fecha = timezone.datetime.strptime(dia, '%Y-%m-%d').date()
            entradas = RegistroEntrada.objects.filter(
                hora_entrada__date=fecha,
                visitante__visita_activa=False
            ).order_by('-hora_entrada')
        except ValueError:
            error = "Formato de fecha inválido (usa YYYY-MM-DD)."
            entradas = []
    else:
        entradas = []

    # Asociar salida a cada entrada
    visitas = []
    for entrada in entradas:
        salida = entrada.visitante.salidas.filter(hora_salida__gt=entrada.hora_entrada).order_by('hora_salida').first()
        visitas.append({
            'entrada': entrada,
            'salida': salida
        })

    return render(request, 'visitantes/busquedaVisitantes.html', {
    'visitas': visitas,
    'rut': rut_formateado,
    'dia': dia,
    'error': error,
    })

#busqueda por rut estandarizada

import re

def formatea_rut(rut):
    "estandarisa el rut independiente lo que ponga en la casilla"
    rut = rut.replace(".", "").replace("-", "").replace(" ", "").upper()
    if len(rut) < 2:
        return rut
    cuerpo = rut[:-1]
    dv = rut[-1]
    # Pone puntos cada 3 dígitos desde la derecha
    cuerpo = cuerpo[::-1]
    cuerpo = '.'.join([cuerpo[i:i+3] for i in range(0, len(cuerpo), 3)])
    cuerpo = cuerpo[::-1]
    return f"{cuerpo}-{dv}"