from django.shortcuts import render
from django.utils import timezone

# Importamos el modelo Promocion para pasar las promociones al template
try:
    from promociones.models import Promocion
except Exception:
    Promocion = None
 
# Importamos Categoria para mostrar el grid de categorías
try:
    from producto.models import Categoria
    try:
        from producto.models import Marca
    except Exception:
        Marca = None
except Exception:
    Categoria = None


def home(request):
    """Vista principal. Añade promociones activas (si existen) al contexto para
    que el include del carrusel las muestre en home.html.
    """
    promociones = []
    if Promocion is not None:
        ahora = timezone.now()
        qs = Promocion.objects.filter(fecha_inicio__lte=ahora, fecha_fin__gte=ahora)
        if not qs.exists():
            qs = Promocion.objects.all()[:6]
        promociones = qs

    categorias = []
    if Categoria is not None:
        categorias = Categoria.objects.all()[:12]  # limitar a 12 categorías para el grid

    # Obtener marcas para mostrar en home (limitamos a 8 por fila/espacio)
    marcas = []
    if Marca is not None:
        marcas = Marca.objects.all()[:12]

    # Añadir formulario de inicio de sesión al contexto para poder incluirlo en home
    try:
        from inicio_sesion.forms import LoginForm
        login_form = LoginForm()
    except Exception:
        login_form = None

    return render(request, 'home.html', {'promociones': promociones, 'categorias': categorias, 'marcas': marcas, 'login_form': login_form})