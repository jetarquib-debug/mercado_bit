from django.shortcuts import render
from .models import Promocion
from django.utils import timezone


def promociones(request):
    """Renderiza la plantilla del carrusel de promociones.

    Se seleccionan las promociones activas por fecha. Si no hay promociones activas,
    se devuelven las más recientes (ordering definido en el modelo).
    Contexto devuelto:
      - promociones: queryset de objetos Promocion
      - autoplay_interval_ms: entero (milisegundos) opcional para el JS
    """
    ahora = timezone.now()
    promociones_qs = Promocion.objects.filter(fecha_inicio__lte=ahora, fecha_fin__gte=ahora)

    if not promociones_qs.exists():
        # fallback: mostrar las promociones más recientes (limit 6 para seguridad)
        promociones_qs = Promocion.objects.all()[:6]

    context = {
        'promociones': promociones_qs,
        'autoplay_interval_ms': 5000,  # puedes ajustar desde la vista si quieres
    }

    return render(request, 'promociones_carousel.html', context)