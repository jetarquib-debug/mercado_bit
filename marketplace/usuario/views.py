from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Usuario


def perfil_usuario(request):
	usuario_id = request.session.get('usuario_id')
	if not usuario_id:
		messages.info(request, 'Debes iniciar sesión para ver tu perfil.')
		return redirect('inicio_sesion:login')

	usuario = get_object_or_404(Usuario, pk=usuario_id)

	context = {
		'usuario': usuario,
	}
	return render(request, 'perfil_usuario.html', context)


# --------------------
# API (DRF) ViewSets
# --------------------
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import UsuarioSerializer, UsuarioSerializerMinimal
from marketplace.permissions import IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly
from marketplace.throttles import UserBurstRateThrottle, AnonBurstRateThrottle


class UsuarioViewSet(mixins.ListModelMixin,
					 mixins.RetrieveModelMixin,
					 mixins.UpdateModelMixin,
					 viewsets.GenericViewSet):
	queryset = Usuario.objects.all()
	serializer_class = UsuarioSerializer
	permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
	throttle_classes = (UserBurstRateThrottle, AnonBurstRateThrottle)

	def get_serializer_class(self):
		if self.action == 'list':
			return UsuarioSerializerMinimal
		return UsuarioSerializer

	@action(detail=True, methods=['post'])
	def set_password(self, request, pk=None):
		usuario = self.get_object()
		pwd = request.data.get('contrasena')
		if not pwd:
			return Response({'detail': 'contrasena requerida.'}, status=status.HTTP_400_BAD_REQUEST)
		usuario.contrasena = pwd
		usuario.save()
		return Response({'detail': 'Contraseña actualizada.'})
