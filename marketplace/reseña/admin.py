from django.contrib import admin
from .models import Resena


@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ('producto', 'usuario', 'puntuacion', 'fecha_creacion', 'is_active')
    list_filter = ('puntuacion', 'fecha_creacion', 'is_active')
    search_fields = ('producto__nomb_prod', 'usuario__email', 'comentario')
from django.contrib import admin

# Register your models here.
