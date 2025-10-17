from django.contrib import admin
from django.utils.html import format_html
from .models import Tienda, ImagenPerfilTienda


# --- INLINE: mostrar imágenes dentro de la tienda ---
class ImagenPerfilTiendaInline(admin.TabularInline):
    model = Tienda.imagenes.through  # relación ManyToMany
    extra = 1
    verbose_name = "Imagen de la tienda"
    verbose_name_plural = "Imágenes de la tienda"


# --- ADMIN para ImagenPerfilTienda ---
@admin.register(ImagenPerfilTienda)
class ImagenPerfilTiendaAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'es_principal', 'fecha_subida', 'vista_previa')
    list_filter = ('es_principal', 'fecha_subida')
    search_fields = ('imagen',)
    ordering = ('-es_principal', '-fecha_subida')
    readonly_fields = ('vista_previa',)

    def vista_previa(self, obj):
        """Muestra una vista previa de la imagen en el panel de admin."""
        if obj.imagen:
            return format_html(
                '<img src="{}" width="80" style="border-radius:8px; box-shadow:0 0 4px rgba(0,0,0,0.2);"/>',
                obj.imagen.url
            )
        return "(Sin imagen)"
    vista_previa.short_description = "Vista previa"


# --- ADMIN para Tienda ---
@admin.register(Tienda)
class TiendaAdmin(admin.ModelAdmin):
    list_display = (
        'vista_miniatura',  # 👈 nueva columna de imagen
        'nombre_tienda',
        'usuario',
        'email',
        'telefono_formateado',
        'ubicacion_completa',
        'fecha_registro',
        'imagenes_contador',
    )
    list_display_links = ('vista_miniatura', 'nombre_tienda')
    list_filter = ('pais', 'departamento', 'provincia', 'fecha_registro')
    search_fields = ('nombre_tienda', 'usuario__email', 'email', 'ruc')
    readonly_fields = (
        'fecha_registro',
        'vista_imagen_principal',
        'ubicacion_completa',
        'imagenes_contador',
    )
    inlines = [ImagenPerfilTiendaInline]

    fieldsets = (
        ("Información General", {
            'fields': (
                'nombre_tienda', 'descripcion', 'email', 'ruc', 'usuario',
                'fecha_registro', 'vista_imagen_principal'
            )
        }),
        ("Ubicación y Contacto", {
            'fields': (
                'codigo_pais', 'telefono', 'direccion',
                'distrito', 'provincia', 'departamento', 'pais',
                'ubicacion_completa'
            )
        }),
        ("Imágenes", {
            'fields': ('imagenes', 'imagenes_contador')
        }),
    )

    filter_horizontal = ('imagenes',)

    # --- MINIATURA EN LA LISTA ---
    def vista_miniatura(self, obj):
        """Muestra la imagen principal como miniatura en la lista."""
        if obj.imagen_principal:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit:cover; border-radius:6px; box-shadow:0 0 3px rgba(0,0,0,0.3);"/>',
                obj.imagen_principal
            )
        return format_html(
            '<div style="width:50px; height:50px; border-radius:6px; background:#eee; display:flex; align-items:center; justify-content:center; color:#999;">—</div>'
        )
    vista_miniatura.short_description = "Imagen"

    # --- VISTA PREVIA DETALLADA ---
    def vista_imagen_principal(self, obj):
        """Vista previa de la imagen principal en el panel de detalle."""
        if obj.imagen_principal:
            return format_html(
                '<img src="{}" width="150" style="border-radius:10px; box-shadow:0 0 6px rgba(0,0,0,0.3);"/>',
                obj.imagen_principal
            )
        return "(Sin imagen principal)"
    vista_imagen_principal.short_description = "Imagen principal"

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
