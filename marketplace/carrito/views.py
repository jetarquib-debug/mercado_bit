from django.shortcuts import render


def ver_carrito(request):
	"""Render view for carrito page. Cart is managed client-side via localStorage."""
	return render(request, 'carrito/carrito.html')

# Create your views here.


# --------------------
# API (DRF) ViewSets
# --------------------
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import CarritoSerializer
from .models import Carrito
from detalles_pedidos.serializers import DetalleOrdenSerializer
from django.db import transaction
from marketplace.permissions import IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly
from marketplace.throttles import UserBurstRateThrottle, AnonBurstRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from marketplace.pagination import StandardPageNumberPagination


class CarritoViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin):
	queryset = Carrito.objects.all().prefetch_related('detalles')
	serializer_class = CarritoSerializer
	permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
	throttle_classes = (UserBurstRateThrottle, AnonBurstRateThrottle)
	filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
	search_fields = ('usuario__email',)
	ordering_fields = ('fecha_creacion',)
	pagination_class = StandardPageNumberPagination

	@action(detail=True, methods=['post'])
	def add_item(self, request, pk=None):
		carrito = self.get_object()
		data = request.data.copy()
		data['carrito'] = carrito.id
		serializer = DetalleOrdenSerializer(data=data)
		serializer.is_valid(raise_exception=True)
		try:
			with transaction.atomic():
				detalle = serializer.save()
		except Exception as e:
			return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
		return Response(DetalleOrdenSerializer(detalle).data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@action(detail=True, methods=['post'])
	def clear(self, request, pk=None):
		carrito = self.get_object()
		carrito.detalles.all().delete()
		return Response({'detail': 'Carrito limpiado.'})

	@action(detail=True, methods=['post'])
	def checkout(self, request, pk=None):
		# acción simple: crear una orden basada en el carrito y devolverla
		from detalle_orden.models import Orden
		carrito = self.get_object()
		try:
			with transaction.atomic():
				orden = Orden.objects.create(carrito=carrito, total=0)
				orden.calcular_total()
		except Exception as e:
			return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
		return Response({'orden_id': orden.id, 'total': orden.total})
