from django.contrib import admin
from django.utils.html import format_html
from .models import MetodoPago


@admin.register(MetodoPago)
class MetodoPagoAdmin(admin.ModelAdmin):
    list_display = ("nomb_meto", "vista_previa",)
    search_fields = ("nomb_meto",)
    list_per_page = 10
    ordering = ("nomb_meto",)
    readonly_fields = ("vista_previa",)
    fieldsets = (
        ("Información del Método de Pago", {
            "fields": ("nomb_meto", "imagen_metodo", "vista_previa")
        }),
    )

    def vista_previa(self, obj):
        """Vista previa de la imagen en el panel de administración."""
        if obj.imagen_metodo:
            return format_html(
                '<img src="{}" width="80" style="border-radius:10px; box-shadow:0 0 6px rgba(0,0,0,0.2);" />',
                obj.imagen_metodo.url
            )
        return "(Sin imagen)"
    vista_previa.short_description = "Vista previa"

    class Media:
        css = {
            "all": ("admin/css/custom_admin.css",)
        }
