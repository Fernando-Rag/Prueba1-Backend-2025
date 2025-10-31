from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .models import Visitante, RegistroEntrada, RegistroSalida


class RegistroEntradaInline(admin.TabularInline):
    #Mostrar entradas relacionadas dentro del Visitante

    model = RegistroEntrada
    extra = 0
    readonly_fields = ("hora_entrada", "motivo")
    can_delete = False
    verbose_name = _("Entrada")
    verbose_name_plural = _("Entradas")


class RegistroSalidaInline(admin.TabularInline):
    #Mostrar salidas relacionadas dentro del Visitante

    model = RegistroSalida
    extra = 0
    readonly_fields = ("hora_salida",)
    can_delete = False
    verbose_name = _("Salida")
    verbose_name_plural = _("Salidas")


@admin.action(description="Marcar visita(s) seleccionada(s) como activa(s)")
def marcar_como_activa(modeladmin, request, queryset):
    updated = queryset.update(visita_activa=True)
    modeladmin.message_user(
        request,
        _("%d visitante(s) marcad%s como con visita activa.") % (updated, "o" if updated == 1 else "s"),
        messages.SUCCESS,
    )


@admin.action(description="Marcar visita(s) seleccionada(s) como no activa(s)")
def marcar_como_inactiva(modeladmin, request, queryset):
    updated = queryset.update(visita_activa=False)
    modeladmin.message_user(
        request,
        _("%d visitante(s) marcad%s como sin visita activa.") % (updated, "o" if updated == 1 else "s"),
        messages.SUCCESS,
    )


class EdadRangeFilter(admin.SimpleListFilter):
    #Filtro personalizado por rangos de edad. Ejemplos: 0-17 (menores), 18-40, 41-65, 66+

    title = _("Rango de edad")
    parameter_name = "rango_edad"

    def lookups(self, request, model_admin):
        return [
            ("menor", _("0 - 17")),
            ("joven", _("18 - 40")),
            ("adulto", _("41 - 65")),
            ("mayor", _("66+")),
        ]

    def queryset(self, request, queryset):
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
        # no permitir editar visita_activa desde el formulario del visitante si es superusuario:
        # (ejemplo de personalización; ajustar según reglas de negocio)
        
        ro = list(getattr(self, "readonly_fields", ()))
        if obj is not None and obj.visita_activa:
            # opcional: mostrar como solo lectura el campo visita_activa cuando está activo
            ro.append("visita_activa")
        return ro


class VisitanteLookupMixin:
    """Mixin para buscar por campos del visitante en admin de registros"""
    search_fields = ("visitante__nombre_s", "visitante__apellido_s", "visitante__rut")
    # mostrar enlace al visitante en list_display si se desea
    def visitante_display(self, obj):
        return str(obj.visitante)
    visitante_display.short_description = _("Visitante")
    visitante_display.admin_order_field = "visitante__apellido_s"


@admin.register(RegistroEntrada)
class RegistroEntradaAdmin(admin.ModelAdmin, VisitanteLookupMixin):
    list_display = ("visitante_display", "motivo", "hora_entrada")
    search_fields = VisitanteLookupMixin.search_fields + ("motivo",)
    list_filter = ("hora_entrada", "motivo")
    date_hierarchy = "hora_entrada"
    ordering = ("-hora_entrada",)
    readonly_fields = ("hora_entrada",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # seleccionar visitante relacionado para evitar consultas N+1
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