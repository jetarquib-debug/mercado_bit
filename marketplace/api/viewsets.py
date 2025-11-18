from rest_framework import viewsets, mixins, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .filters import ProductoFilterSet, TiendaFilterSet, PromocionFilterSet, UsuarioFilterSet
from .pagination import StandardLimitOffsetPagination

from .permissions import IsObjectOwnerOrReadOnly

from producto.models import Producto
from producto.serializers import ProductoSerializer
from usuario.models import Usuario
from usuario.serializers import UsuarioSerializer
from tienda.models import Tienda
from tienda.serializers import TiendaSerializer
from carrito.models import Carrito
from carrito.serializers import CarritoSerializer
from detalles_pedidos.models import DetalleOrden
from detalles_pedidos.serializers import DetalleOrdenSerializer
from detalle_orden.models import Orden
from detalle_orden.serializers import OrdenSerializer
from pago.models import Pago, MetodoPago
from pago.serializers import PagoSerializer, MetodoPagoSerializer
from promociones.models import Promocion
from promociones.serializers import PromocionSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all().select_related('marca', 'tienda').prefetch_related('categoria', 'imagenes')
    serializer_class = ProductoSerializer
    # Lectura abierta, escrituras restringidas a usuarios autenticados + object-level
    permission_classes = [IsAuthenticatedOrReadOnly, IsObjectOwnerOrReadOnly]
    throttle_classes = [ScopedRateThrottle, UserRateThrottle, AnonRateThrottle]
    throttle_scope = 'productos'
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductoFilterSet
    search_fields = ['nomb_prod', 'descripcion', 'marca__nomb_marca']
    ordering_fields = ['precio', 'stock', 'fecha_creacion']
    # usar paginación limit-offset para listados grandes
    pagination_class = StandardLimitOffsetPagination

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        qs = self.get_queryset().filter(stock__lte=5)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def set_stock(self, request, pk=None):
        producto = self.get_object()
        stock = request.data.get('stock')
        try:
            stock = int(stock)
        except (TypeError, ValueError):
            return Response({'detail': 'Stock inválido.'}, status=status.HTTP_400_BAD_REQUEST)
        producto.stock = stock
        producto.save()
        return Response(self.get_serializer(producto).data)


class UsuarioViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = Usuario.objects.all().prefetch_related('imagenes')
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsObjectOwnerOrReadOnly]
    throttle_classes = [ScopedRateThrottle, UserRateThrottle, AnonRateThrottle]
    throttle_scope = 'usuarios'
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = UsuarioFilterSet
    search_fields = ['nombres', 'apellidos', 'email']
    ordering_fields = ['fecha_registro', 'nombres']

    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        usuario = self.get_object()
        contrasena = request.data.get('contrasena')
        if not contrasena:
            return Response({'detail': 'contrasena required'}, status=status.HTTP_400_BAD_REQUEST)
        usuario.contrasena = contrasena
        usuario.save()
        return Response({'detail': 'password updated'})


class TiendaViewSet(viewsets.ModelViewSet):
    queryset = Tienda.objects.all().prefetch_related('imagenes')
    serializer_class = TiendaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsObjectOwnerOrReadOnly]
    throttle_classes = [ScopedRateThrottle, UserRateThrottle, AnonRateThrottle]
    throttle_scope = 'tiendas'
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TiendaFilterSet
    search_fields = ['nombre_tienda', 'descripcion']
    ordering_fields = ['nombre_tienda', 'fecha_registro']

    @action(detail=True, methods=['get'])
    def productos(self, request, pk=None):
        tienda = self.get_object()
        productos = tienda.productos.all().select_related('marca')
        serializer = ProductoSerializer(productos, many=True, context={'request': request})
        return Response(serializer.data)


class CarritoViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsObjectOwnerOrReadOnly]
    throttle_classes = [ScopedRateThrottle, UserRateThrottle, AnonRateThrottle]
    throttle_scope = 'carritos'
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['usuario__email']
    ordering_fields = ['fecha_creacion']

    @action(detail=True, methods=['post'])
    def clear(self, request, pk=None):
        carrito = self.get_object()
        if hasattr(carrito, 'detalles'):
            carrito.detalles.all().delete()
        return Response({'detail': 'Carrito vaciado'})


class DetalleOrdenViewSet(viewsets.ModelViewSet):
    queryset = DetalleOrden.objects.all().select_related('producto', 'carrito')
    serializer_class = DetalleOrdenSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsObjectOwnerOrReadOnly]
    throttle_classes = [ScopedRateThrottle, UserRateThrottle, AnonRateThrottle]
    throttle_scope = 'detalles'
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['producto__nomb_prod']
    ordering_fields = ['cantidad', 'subtotal']


class OrdenViewSet(viewsets.ModelViewSet):
    queryset = Orden.objects.all().select_related('carrito')
    serializer_class = OrdenSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsObjectOwnerOrReadOnly]
    throttle_classes = [ScopedRateThrottle, UserRateThrottle, AnonRateThrottle]
    throttle_scope = 'ordenes'
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['carrito__usuario__email']
    ordering_fields = ['total', 'fecha_creacion']

    @action(detail=True, methods=['post'])
    def calcular_total(self, request, pk=None):
        orden = self.get_object()
        total = orden.calcular_total()
        return Response({'total': total})

    @action(detail=True, methods=['post'])
    def marcar_entregado(self, request, pk=None):
        orden = self.get_object()
        orden.estado = 'entregado'
        orden.save()
        return Response({'detail': 'Orden marcada como entregada'})


class MetodoPagoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MetodoPago.objects.all()
    serializer_class = MetodoPagoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [ScopedRateThrottle, UserRateThrottle, AnonRateThrottle]
    throttle_scope = 'metodos_pago'
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nomb_meto']
    ordering_fields = ['nomb_meto']


class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all().select_related('metodo', 'orden')
    serializer_class = PagoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsObjectOwnerOrReadOnly]
    throttle_classes = [ScopedRateThrottle, UserRateThrottle, AnonRateThrottle]
    throttle_scope = 'pagos'
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['transaccion_id']
    ordering_fields = ['fecha_pago', 'monto']

    @action(detail=True, methods=['post'])
    def procesar(self, request, pk=None):
        pago = self.get_object()
        pago.procesar_pago()
        return Response({'estado': pago.estado})

    @action(detail=True, methods=['post'])
    def completar(self, request, pk=None):
        pago = self.get_object()
        pago.completar_pago(transaccion_id=request.data.get('transaccion_id'))
        return Response({'estado': pago.estado})


class PromocionViewSet(viewsets.ModelViewSet):
    queryset = Promocion.objects.all().prefetch_related('productos', 'categorias')
    serializer_class = PromocionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [ScopedRateThrottle, UserRateThrottle, AnonRateThrottle]
    throttle_scope = 'promociones'
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PromocionFilterSet
    search_fields = ['descripcion']
    ordering_fields = ['fecha_inicio', 'fecha_fin', 'descuento_porcentaje']

    @action(detail=False, methods=['get'])
    def activas(self, request):
        qs = self.get_queryset().filter(fecha_fin__gte=None) if False else [p for p in self.get_queryset() if p.activa]
        # Serializar manualmente para no romper queryset logic
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
