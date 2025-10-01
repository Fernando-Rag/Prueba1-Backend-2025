from django.shortcuts import render, get_object_or_404, redirect
from .models import Visitante, RegistroEntrada, RegistroSalida
from .forms import VisitanteForm, RegistroEntradaForm, RegistroSalidaForm

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
    entradas = RegistroEntrada.objects.select_related('visitante').all()
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
        error = None
    return render(request, 'visitantes/registroEntrada.html', {'entradas': entradas, 'form': form, 'error': error})

# Registro Salida
def registroSalida(request):
    salidas = RegistroSalida.objects.select_related('visitante').all()
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
        error = None
    return render(request, 'visitantes/registroSalida.html', {'salidas': salidas, 'form': form, 'error': error})

# Búsqueda de visitantes
def busquedaVisitantes(request):
    visitantes = []
    query = request.GET.get('q', '')
    if query:
        visitantes = Visitante.objects.filter(
            nombre_s__icontains=query
        ) | Visitante.objects.filter(
            apellido_s__icontains=query
        ) | Visitante.objects.filter(
            rut__icontains=query
        )
    return render(request, 'visitantes/busquedaVisitantes.html', {'visitantes': visitantes, 'query': query})