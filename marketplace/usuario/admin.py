from django.contrib import admin
from .models import (
    ImagenPerfilUsuario,
    Pais, Departamento, Provincia, Distrito,
    CodigoPais,
    Usuario
)

# ==============================
# 📸 IMAGEN PERFIL USUARIO
# ==============================
@admin.register(ImagenPerfilUsuario)
class ImagenPerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'vista_previa', 'es_principal', 'fecha_subida')
    list_filter = ('es_principal', 'fecha_subida')
    readonly_fields = ('vista_previa',)
    search_fields = ('id',)
    ordering = ('-fecha_subida',)

    fieldsets = (
        ('Información de Imagen', {
            'fields': ('imagen', 'vista_previa', 'es_principal')
        }),
        ('Metadatos', {
            'fields': ('fecha_subida',),
        }),
    )


# ==============================
# 🌍 UBICACIÓN GEOGRÁFICA
# ==============================
@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ('nomb_pais',)
    search_fields = ('nomb_pais',)
    ordering = ('nomb_pais',)


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('nomb_departamento', 'pais')
    list_filter = ('pais',)
    search_fields = ('nomb_departamento', 'pais__nomb_pais')
    ordering = ('nomb_departamento',)


@admin.register(Provincia)
class ProvinciaAdmin(admin.ModelAdmin):
    list_display = ('nomb_provincia', 'departamento')
    list_filter = ('departamento',)
    search_fields = ('nomb_provincia', 'departamento__nomb_departamento')
    ordering = ('nomb_provincia',)


@admin.register(Distrito)
class DistritoAdmin(admin.ModelAdmin):
    list_display = ('nomb_distrito', 'provincia')
    list_filter = ('provincia',)
    search_fields = ('nomb_distrito', 'provincia__nomb_provincia')
    ordering = ('nomb_distrito',)


# ==============================
# ☎️ CÓDIGO DE PAÍS
# ==============================
@admin.register(CodigoPais)
class CodigoPaisAdmin(admin.ModelAdmin):
    list_display = ('pais', 'codigo', 'bandera')
    readonly_fields = ('bandera',)
    search_fields = ('pais__nomb_pais', 'codigo')
    ordering = ('pais__nomb_pais',)
    fieldsets = (
        ('Información del País', {
            'fields': ('pais', 'codigo', 'imagen_pais', 'bandera')
        }),
    )


# ==============================
# 👤 USUARIO
# ==============================
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('vista_previa', 'nombres', 'apellidos', 'email', 'codigo_pais', 'telefono', 'pais', 'departamento', 'provincia', 'fecha_registro')
    list_filter = ('sexo', 'fecha_registro', 'codigo_pais', 'pais', 'departamento')
    search_fields = ('nombres', 'apellidos', 'email', 'telefono', 'pais__nomb_pais', 'departamento__nomb_departamento')
    readonly_fields = ('vista_previa',)
    ordering = ('-fecha_registro',)

    fieldsets = (
        ('Información Personal', {
            'fields': ('vista_previa', 'nombres', 'apellidos', 'email', 'contrasena', 'sexo', 'dni_ce')
        }),
        ('Ubicación y Contacto', {
            'fields': ('codigo_pais', 'telefono', 'direccion', 'pais', 'departamento', 'provincia', 'distrito')
        }),
        ('Imágenes', {
            'fields': ('imagenes',)
        }),
        ('Fechas', {
            'fields': ('fecha_registro',),
        }),
    )
