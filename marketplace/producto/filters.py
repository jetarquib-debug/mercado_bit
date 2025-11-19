import django_filters
from .models import Producto


class ProductoFilter(django_filters.FilterSet):
    precio_min = django_filters.NumberFilter(field_name='precio', lookup_expr='gte')
    precio_max = django_filters.NumberFilter(field_name='precio', lookup_expr='lte')
    tienda = django_filters.NumberFilter(field_name='tienda__id', lookup_expr='exact')
    marca = django_filters.NumberFilter(field_name='marca__id', lookup_expr='exact')
    estado = django_filters.CharFilter(field_name='estado', lookup_expr='exact')

    class Meta:
        model = Producto
        fields = ['tienda', 'marca', 'categoria', 'estado', 'precio_min', 'precio_max']
