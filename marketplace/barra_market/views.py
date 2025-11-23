from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse

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
        try:
            qs = Promocion.objects.filter(fecha_inicio__lte=ahora, fecha_fin__gte=ahora)
            if not qs.exists():
                qs = Promocion.objects.all()[:6]
            promociones = qs
        except Exception:
            # Si la consulta falla (p. ej. columna faltante por migraciones pendientes),
            # devolvemos un fallback silencioso para evitar 500s en la página principal.
            try:
                promociones = Promocion.objects.all()[:6]
            except Exception:
                promociones = []

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


def api_categorias_marcas(request):
    """Endpoint JSON que devuelve las categorías y marcas.

    Motivo de la adición: en algunos templates el context processor puede
    no entregar las variables (p. ej. por errores de import en tiempo de
    ejecución). Este endpoint permite que el frontend haga una petición
    y obtenga los datos de forma fiable (fallback dinámico).
    """
    try:
        from producto.models import Categoria, Marca
        categorias_qs = Categoria.objects.all().order_by('nomb_ca')
        marcas_qs = Marca.objects.all().order_by('nomb_marca')
        categorias = [{'id': c.pk, 'nomb_ca': c.nomb_ca} for c in categorias_qs]
        marcas = [{'id': m.pk, 'nomb_marca': m.nomb_marca} for m in marcas_qs]
    except Exception:
        # En caso de fallo devolvemos listas vacías en vez de 500.
        categorias = []
        marcas = []

    return JsonResponse({'categorias': categorias, 'marcas': marcas})