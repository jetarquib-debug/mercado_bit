from django.contrib import admin
from .models import Tienda, ImagenPerfilTienda


# --- INLINE: mostrar imágenes dentro de la tienda ---
class ImagenPerfilTiendaInline(admin.TabularInline):
    model = Tienda.imagenes.through  # relación ManyToMany
    extra = 1
    verbose_name = "Imagen de la tienda"
    verbose_name_plural = "Imágenes de la tienda"
    autocomplete_fields = ['imagenperfiltineda']


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
            return f'<img src="{obj.imagen.url}" width="80" style="border-radius:8px;"/>'
        return "(Sin imagen)"
    vista_previa.allow_tags = True
    vista_previa.short_description = "Vista previa"


# --- ADMIN para Tienda ---
@admin.register(Tienda)
class TiendaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre_tienda', 'usuario', 'email', 'telefono_formateado',
        'ubicacion_completa', 'fecha_registro', 'imagenes_contador'
    )
    list_filter = ('pais', 'departamento', 'provincia', 'fecha_registro')
    search_fields = ('nombre_tienda', 'usuario__email', 'email', 'ruc')
    readonly_fields = ('fecha_registro', 'vista_imagen_principal', 'ubicacion_completa', 'imagenes_contador')
    inlines = []  # Podrías añadir ImagenPerfilTiendaInline aquí si prefieres verlas dentro de la tienda

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

    def vista_imagen_principal(self, obj):
        """Vista previa de la imagen principal en el panel."""
        if obj.imagen_principal:
            return f'<img src="{obj.imagen_principal}" width="100" style="border-radius:10px;"/>'
        return "(Sin imagen principal)"
    vista_imagen_principal.allow_tags = True
    vista_imagen_principal.short_description = "Imagen principal"

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
