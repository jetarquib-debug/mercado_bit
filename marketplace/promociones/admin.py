from django.contrib import admin
from django.utils.html import format_html
from .models import Promocion


@admin.register(Promocion)
class PromocionAdmin(admin.ModelAdmin):
    list_display = (
        "descripcion",
        "descuento_porcentaje",
        "metodo_pago",
        "fecha_inicio",
        "fecha_fin",
        "activa_coloreada",
        "vista_previa",
    )
    list_filter = ("metodo_pago", "fecha_inicio", "fecha_fin")
    search_fields = ("descripcion", "metodo_pago__nomb_meto")
    ordering = ("-fecha_inicio",)
    readonly_fields = ("vista_previa", "activa_coloreada", "dias_restantes")
    filter_horizontal = ("productos", "categorias")

    fieldsets = (
        ("Detalles Generales", {
            "fields": (
                "descripcion",
                "descuento_porcentaje",
                "metodo_pago",
                "imagen_promocion",
                "vista_previa",
                "activa_coloreada",
                "dias_restantes",
            )
        }),
        ("Aplicaciones", {
            "fields": ("productos", "categorias")
        }),
        ("Fechas", {
            "fields": ("fecha_inicio", "fecha_fin")
        }),
    )

    def activa_coloreada(self, obj):
        """Muestra si la promoción está activa con color."""
        color = "green" if obj.activa else "red"
        texto = "Activa" if obj.activa else "Expirada"
        return format_html(f'<b style="color:{color};">{texto}</b>')
    activa_coloreada.short_description = "Estado"

    def vista_previa(self, obj):
        """Vista previa de la imagen de la promoción."""
        if obj.imagen_promocion:
            return format_html(
                '<img src="{}" width="120" style="border-radius:10px; box-shadow:0 0 6px rgba(0,0,0,0.2);"/>',
                obj.imagen_promocion.url
            )
        return "(Sin imagen)"
    vista_previa.short_description = "Vista previa"

    class Media:
        css = {
            "all": ("admin/css/custom_admin.css",)
        }
