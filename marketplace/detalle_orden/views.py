from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Orden
from .serializers import OrdenSerializer
from marketplace.permissions import IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly
from marketplace.throttles import UserBurstRateThrottle, AnonBurstRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from marketplace.pagination import StandardPageNumberPagination


class OrdenViewSet(viewsets.ModelViewSet):
	queryset = Orden.objects.all().select_related('carrito')
	serializer_class = OrdenSerializer
	permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
	throttle_classes = (UserBurstRateThrottle, AnonBurstRateThrottle)
	filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
	search_fields = ('carrito__usuario__email',)
	ordering_fields = ('fecha_creacion', 'total')
	pagination_class = StandardPageNumberPagination

	@action(detail=True, methods=['post'])
	def recalculate(self, request, pk=None):
		orden = self.get_object()
		total = orden.calcular_total()
		return Response({'total': total})

	@action(detail=True, methods=['post'])
	def mark_entregado(self, request, pk=None):
		orden = self.get_object()
		orden.estado = 'entregado'
		orden.save(update_fields=['estado'])
		return Response({'detail': 'Orden marcada como entregada.'})
