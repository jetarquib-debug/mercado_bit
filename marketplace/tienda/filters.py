import django_filters
from .models import Tienda


class TiendaFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(field_name='nombre_tienda', lookup_expr='icontains')
    fecha_registro_after = django_filters.DateTimeFilter(field_name='fecha_registro', lookup_expr='gte')
    fecha_registro_before = django_filters.DateTimeFilter(field_name='fecha_registro', lookup_expr='lte')

    class Meta:
        model = Tienda
        fields = ['nombre', 'codigo_pais', 'pais', 'fecha_registro_after', 'fecha_registro_before']
