from django.shortcuts import render
from django.utils import timezone

# Importamos el modelo Promocion para pasar las promociones al template
try:
    from promociones.models import Promocion
except Exception:
    Promocion = None


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

    return render(request, 'home.html', {'promociones': promociones})