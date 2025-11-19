import django_filters
from .models import Promocion


class PromocionFilter(django_filters.FilterSet):
    fecha_inicio_after = django_filters.DateTimeFilter(field_name='fecha_inicio', lookup_expr='gte')
    fecha_fin_before = django_filters.DateTimeFilter(field_name='fecha_fin', lookup_expr='lte')
    descuento_min = django_filters.NumberFilter(field_name='descuento_porcentaje', lookup_expr='gte')
    descuento_max = django_filters.NumberFilter(field_name='descuento_porcentaje', lookup_expr='lte')

    class Meta:
        model = Promocion
        fields = ['productos', 'categorias', 'fecha_inicio_after', 'fecha_fin_before', 'descuento_min', 'descuento_max']
