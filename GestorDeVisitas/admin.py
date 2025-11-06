from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .models import Visitante, RegistroEntrada, RegistroSalida


# Configuración visual del sitio admin (títulos en español)
admin.site.site_header = "Administración - Control de Visitantes"
admin.site.site_title = "Panel de Administración"
admin.site.index_title = "Sitio de Administración"


class RegistroEntradaInline(admin.TabularInline):
    # Mostrar entradas relacionadas dentro del Visitante
    model = RegistroEntrada
    extra = 0
    readonly_fields = ("hora_entrada", "motivo")
    can_delete = False
    verbose_name = _("Entrada")
    verbose_name_plural = _("Entradas")


class RegistroSalidaInline(admin.TabularInline):
    # Mostrar salidas relacionadas dentro del Visitante
    model = RegistroSalida
    extra = 0
    readonly_fields = ("hora_salida",)
    can_delete = False
    verbose_name = _("Salida")
    verbose_name_plural = _("Salidas")


@admin.action(description="Marcar visita(s) seleccionada(s) como activa(s)")
def marcar_como_activa(modeladmin, request, queryset):
    # Actualiza en bloque el campo visita_activa a True para los objetos seleccionados.
    updated = queryset.update(visita_activa=True)
    # message_user muestra un mensaje en la interfaz del admin (aquí en español).
    modeladmin.message_user(
        request,
        _("%d visitante(s) marcad%s como con visita activa.") % (updated, "o" if updated == 1 else "s"),
        messages.SUCCESS,
    )


@admin.action(description="Marcar visita(s) seleccionada(s) como no activa(s)")
def marcar_como_inactiva(modeladmin, request, queryset):
    # Actualiza en bloque el campo visita_activa a False para los objetos seleccionados.
    updated = queryset.update(visita_activa=False)
    modeladmin.message_user(
        request,
        _("%d visitante(s) marcad%s como sin visita activa.") % (updated, "o" if updated == 1 else "s"),
        messages.SUCCESS,
    )


class EdadRangeFilter(admin.SimpleListFilter):
    # Filtro personalizado por rangos de edad. Ejemplos: 0-17 (menores), 18-40, 41-65, 66+
    title = _("Rango de edad")
    parameter_name = "rango_edad"

    def lookups(self, request, model_admin):
        # Opciones que aparecen en la barra lateral del admin.
        return [
            ("menor", _("0 - 17")),
            ("joven", _("18 - 40")),
            ("adulto", _("41 - 65")),
            ("mayor", _("66+")),
        ]

    def queryset(self, request, queryset):
        # Aplica el filtrado según la opción seleccionada.
        val = self.value()
        if val == "menor":
            return queryset.filter(edad__lte=17)
        if val == "joven":
            return queryset.filter(edad__gte=18, edad__lte=40)
        if val == "adulto":
            return queryset.filter(edad__gte=41, edad__lte=65)
        if val == "mayor":
            return queryset.filter(edad__gte=66)
        return queryset


@admin.register(Visitante)
class VisitanteAdmin(admin.ModelAdmin):
    list_display = ("nombre_s", "apellido_s", "rut", "edad", "visita_activa")
    list_display_links = ("nombre_s", "apellido_s")
    search_fields = ("nombre_s", "apellido_s", "rut")
    # Añadimos filtro por booleano y filtro personalizado por rango de edad
    list_filter = ("visita_activa", EdadRangeFilter)
    ordering = ("apellido_s", "nombre_s")
    inlines = (RegistroEntradaInline, RegistroSalidaInline)
    actions = (marcar_como_activa, marcar_como_inactiva)
    list_per_page = 25

    fieldsets = (
        (None, {"fields": ("nombre_s", "apellido_s", "rut")}),
        (_("Detalles"), {"fields": ("edad", "visita_activa")}),
    )

    def get_readonly_fields(self, request, obj=None):
        # Devuelve campos de solo lectura de forma dinámica.
        # Ejemplo: si el visitante tiene visita_activa=True, mostramos ese campo como solo lectura.
        ro = list(getattr(self, "readonly_fields", ()))
        if obj is not None and obj.visita_activa:
            ro.append("visita_activa")
        return ro


class VisitanteLookupMixin:
    """Mixin para buscar por campos del visitante en admin de registros"""
    # Permite buscar registros (entradas/salidas) usando campos del visitante relacionado.
    search_fields = ("visitante__nombre_s", "visitante__apellido_s", "visitante__rut")

    def visitante_display(self, obj):
        # Muestra el visitante como texto legible en list_display de registros
        return str(obj.visitante)
    visitante_display.short_description = _("Visitante")
    visitante_display.admin_order_field = "visitante__apellido_s"


@admin.register(RegistroEntrada)
class RegistroEntradaAdmin(admin.ModelAdmin, VisitanteLookupMixin):
    list_display = ("visitante_display", "motivo", "hora_entrada")
    # Permite búsqueda por campos del visitante y por motivo
    search_fields = VisitanteLookupMixin.search_fields + ("motivo",)
    list_filter = ("hora_entrada", "motivo")
    # Navegación por fecha (años/meses/días) en la parte superior
    date_hierarchy = "hora_entrada"
    ordering = ("-hora_entrada",)
    readonly_fields = ("hora_entrada",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # select_related evita consultas N+1 trayendo el visitante en la misma consulta
        return qs.select_related("visitante")


@admin.register(RegistroSalida)
class RegistroSalidaAdmin(admin.ModelAdmin, VisitanteLookupMixin):
    list_display = ("visitante_display", "hora_salida")
    search_fields = VisitanteLookupMixin.search_fields
    list_filter = ("hora_salida",)
    date_hierarchy = "hora_salida"
    ordering = ("-hora_salida",)
    readonly_fields = ("hora_salida",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("visitante")