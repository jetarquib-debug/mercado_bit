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


# --------------------
# API (DRF) ViewSets
# --------------------
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Promocion
from .serializers import PromocionSerializer
from marketplace.permissions import DjangoModelPermissionsOrAnonReadOnly, IsAuthenticatedOrReadOnly
from marketplace.throttles import UserBurstRateThrottle, AnonBurstRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import PromocionFilter
from marketplace.pagination import StandardPageNumberPagination, StandardLimitOffsetPagination


class PromocionViewSet(viewsets.ModelViewSet):
    queryset = Promocion.objects.all()
    serializer_class = PromocionSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    throttle_classes = (UserBurstRateThrottle, AnonBurstRateThrottle)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = PromocionFilter
    search_fields = ('descripcion',)
    ordering_fields = ('fecha_inicio', 'fecha_fin', 'descuento_porcentaje')
    # permitir tanto paginación por páginas como limit/offset según consulta
    pagination_class = StandardLimitOffsetPagination

    @action(detail=False, methods=['get'])
    def active(self, request):
        ahora = timezone.now()
        qs = Promocion.objects.filter(fecha_inicio__lte=ahora, fecha_fin__gte=ahora)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def preview_apply(self, request, pk=None):
        promo = self.get_object()
        # devolver resumen aplicable
        data = {
            'id': promo.id,
            'descuento_porcentaje': promo.descuento_porcentaje,
            'activa': promo.activa,
        }
        return Response(data)