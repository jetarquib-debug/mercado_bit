from django.shortcuts import render, get_object_or_404
from .models import Tienda
from producto.models import Producto
from django.db.models import Sum, Count


def perfil_tienda(request, pk=None):
	"""Renderiza la página de perfil de la tienda.
	Si se pasa `pk`, carga la Tienda correspondiente; si no, renderiza una vista genérica.
	"""
	tienda = None
	if pk is not None:
		tienda = get_object_or_404(Tienda, pk=pk)

	return render(request, 'perfil_tienda.html', {'tienda': tienda})


def perfil_tienda_comercial(request, pk):
	"""Vista comercial de la tienda: muestra panel con botones para info, productos, stock y acciones comerciales."""
	tienda = get_object_or_404(Tienda, pk=pk)

	# productos de la tienda
	productos_qs = Producto.objects.filter(tienda=tienda).select_related('marca')
	productos = list(productos_qs)

	# estadísticas simples
	total_productos = productos_qs.count()
	en_stock = productos_qs.filter(stock__gt=0).count()
	agotados = productos_qs.filter(stock__lte=0).count()

	return render(request, 'perfil_tienda_comercial.html', {
		'tienda': tienda,
		'productos': productos,
		'total_productos': total_productos,
		'en_stock': en_stock,
		'agotados': agotados,
	})


# --------------------
# API (DRF) ViewSets
# --------------------
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import TiendaSerializer, ImagenPerfilTiendaSerializer
from .models import Tienda, ImagenPerfilTienda
from marketplace.permissions import IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly
from marketplace.throttles import UserBurstRateThrottle, AnonBurstRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import TiendaFilter
from marketplace.pagination import StandardPageNumberPagination


class TiendaViewSet(viewsets.ModelViewSet):
	queryset = Tienda.objects.all().prefetch_related('imagenes')
	serializer_class = TiendaSerializer
	parser_classes = [MultiPartParser, FormParser]
	permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
	throttle_classes = (UserBurstRateThrottle, AnonBurstRateThrottle)
	filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
	filterset_class = TiendaFilter
	search_fields = ('nombre_tienda', 'descripcion')
	ordering_fields = ('nombre_tienda', 'fecha_registro')
	pagination_class = StandardPageNumberPagination

	@action(detail=True, methods=['post'])
	def upload_image(self, request, pk=None):
		tienda = self.get_object()
		serializer = ImagenPerfilTiendaSerializer(data=request.data)
		if serializer.is_valid():
			img = serializer.save()
			tienda.imagenes.add(img)
			return Response({'detail': 'Imagen subida.'}, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@action(detail=True, methods=['get'])
	def stats(self, request, pk=None):
		tienda = self.get_object()
		total_productos = tienda.productos.count()
		en_stock = tienda.productos.filter(stock__gt=0).count()
		return Response({'total_productos': total_productos, 'en_stock': en_stock})
