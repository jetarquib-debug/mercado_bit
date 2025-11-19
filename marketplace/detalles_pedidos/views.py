from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import DetalleOrden
from .serializers import DetalleOrdenSerializer
from django.db import transaction
from marketplace.permissions import IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly
from marketplace.throttles import UserBurstRateThrottle, AnonBurstRateThrottle


class DetalleOrdenViewSet(viewsets.ModelViewSet):
	queryset = DetalleOrden.objects.all().select_related('producto', 'carrito')
	serializer_class = DetalleOrdenSerializer
	permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
	throttle_classes = (UserBurstRateThrottle, AnonBurstRateThrottle)

	@action(detail=True, methods=['post'])
	def update_quantity(self, request, pk=None):
		detalle = self.get_object()
		cantidad = request.data.get('cantidad')
		try:
			cantidad = int(cantidad)
		except Exception:
			return Response({'detail': 'cantidad inválida.'}, status=status.HTTP_400_BAD_REQUEST)
		# validar stock
		if detalle.producto and cantidad > detalle.producto.stock:
			return Response({'detail': 'cantidad supera stock disponible.'}, status=status.HTTP_400_BAD_REQUEST)
		try:
			with transaction.atomic():
				detalle.cantidad = cantidad
				detalle.save()
		except Exception as e:
			return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
		return Response(DetalleOrdenSerializer(detalle).data)
