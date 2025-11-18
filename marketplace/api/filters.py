import django_filters
from django.db.models import Q
from producto.models import Producto
from tienda.models import Tienda
from promociones.models import Promocion
from usuario.models import Usuario


class ProductoFilterSet(django_filters.FilterSet):
    precio_min = django_filters.NumberFilter(field_name='precio', lookup_expr='gte')
    precio_max = django_filters.NumberFilter(field_name='precio', lookup_expr='lte')
    disponible = django_filters.BooleanFilter(method='filter_disponible')
    marca = django_filters.ModelChoiceFilter(field_name='marca', queryset=None)
    tienda = django_filters.ModelChoiceFilter(field_name='tienda', queryset=None)
    categoria = django_filters.ModelMultipleChoiceFilter(field_name='categoria', queryset=None)

    class Meta:
        model = Producto
        fields = ['estado', 'marca', 'tienda', 'categoria', 'precio_min', 'precio_max', 'disponible']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # evitar import circular hasta runtime
        from producto.models import Categoria
        from producto.models import Marca
        from tienda.models import Tienda as TiendaModel
        self.filters['categoria'].queryset = Categoria.objects.all()
        self.filters['marca'].queryset = Marca.objects.all()
        self.filters['tienda'].queryset = TiendaModel.objects.all()

    def filter_disponible(self, queryset, name, value):
        if value:
            return queryset.filter(estado='disponible', stock__gt=0)
        return queryset


class TiendaFilterSet(django_filters.FilterSet):
    nomb = django_filters.CharFilter(field_name='nombre_tienda', lookup_expr='icontains')

    class Meta:
        model = Tienda
        fields = ['nomb', 'pais', 'codigo_pais']


class PromocionFilterSet(django_filters.FilterSet):
    fecha_inicio_after = django_filters.IsoDateTimeFilter(field_name='fecha_inicio', lookup_expr='gte')
    fecha_fin_before = django_filters.IsoDateTimeFilter(field_name='fecha_fin', lookup_expr='lte')
    descuento_min = django_filters.NumberFilter(field_name='descuento_porcentaje', lookup_expr='gte')

    class Meta:
        model = Promocion
        fields = ['productos', 'categorias', 'fecha_inicio_after', 'fecha_fin_before', 'descuento_min']


class UsuarioFilterSet(django_filters.FilterSet):
    nombre = django_filters.CharFilter(method='filter_nombre')

    class Meta:
        model = Usuario
        fields = ['email', 'pais', 'codigo_pais']

    def filter_nombre(self, queryset, name, value):
        return queryset.filter(Q(nombres__icontains=value) | Q(apellidos__icontains=value))
