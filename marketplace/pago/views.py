from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import MetodoPago, Pago
from .serializers import MetodoPagoSerializer, PagoSerializer
from marketplace.permissions import IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly
from marketplace.throttles import UserBurstRateThrottle, AnonBurstRateThrottle
from django.db import transaction


class MetodoPagoViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = MetodoPago.objects.all()
	serializer_class = MetodoPagoSerializer
	permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
	throttle_classes = (UserBurstRateThrottle, AnonBurstRateThrottle)


class PagoViewSet(viewsets.ModelViewSet):
	queryset = Pago.objects.all().select_related('orden', 'metodo')
	serializer_class = PagoSerializer
	permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
	throttle_classes = (UserBurstRateThrottle, AnonBurstRateThrottle)

	@action(detail=True, methods=['post'])
	def procesar(self, request, pk=None):
		pago = self.get_object()
		try:
			with transaction.atomic():
				pago.procesar_pago(monto=request.data.get('monto'))
		except Exception as e:
			return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
		return Response({'estado': pago.estado})

	@action(detail=True, methods=['post'])
	def completar(self, request, pk=None):
		pago = self.get_object()
		trans_id = request.data.get('transaccion_id')
		try:
			with transaction.atomic():
				pago.completar_pago(transaccion_id=trans_id)
		except Exception as e:
			return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
		return Response({'estado': pago.estado})

	@action(detail=True, methods=['post'])
	def reembolsar(self, request, pk=None):
		pago = self.get_object()
		try:
			with transaction.atomic():
				pago.reembolsar()
		except Exception as e:
			return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
		return Response({'estado': pago.estado})

	@action(detail=True, methods=['post'])
	def marcar_fallido(self, request, pk=None):
		pago = self.get_object()
		motivo = request.data.get('motivo')
		try:
			with transaction.atomic():
				pago.marcar_fallido(motivo=motivo)
		except Exception as e:
			return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
		return Response({'estado': pago.estado})
