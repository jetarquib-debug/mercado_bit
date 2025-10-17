from django.contrib import admin
from .models import Marca, Categoria, Producto, ImagenProducto


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nomb_marca', 'vista_previa')
    readonly_fields = ('vista_previa',)
    search_fields = ('nomb_marca',)
    ordering = ('nomb_marca',)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nomb_ca', 'vista_previa')
    readonly_fields = ('vista_previa',)
    search_fields = ('nomb_ca',)
    ordering = ('nomb_ca',)


class ImagenProductoInline(admin.TabularInline):
    model = ImagenProducto
    extra = 1
    readonly_fields = ('vista_previa',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nomb_prod', 'marca', 'precio', 'stock', 'estado', 'vista_previa')
    list_filter = ('estado', 'marca', 'categoria')
    search_fields = ('nomb_prod',)
    readonly_fields = ('vista_previa',)
    inlines = [ImagenProductoInline]


@admin.register(ImagenProducto)
class ImagenProductoAdmin(admin.ModelAdmin):
    list_display = ('producto', 'es_principal', 'fecha_subida', 'vista_previa')
    readonly_fields = ('vista_previa',)
