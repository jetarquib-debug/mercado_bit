from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.urls import reverse

from rest_framework import viewsets, permissions

from .models import Resena
from .serializers import ResenaSerializer
from producto.models import Producto
from usuario.models import Usuario


class ResenaViewSet(viewsets.ModelViewSet):
    queryset = Resena.objects.all()
    serializer_class = ResenaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # intentar asignar usuario si existe una relación por email
        request = self.request
        usuario = None
        try:
            if request.user and request.user.is_authenticated:
                # intentar mapear por email si existe el modelo Usuario
                usuario = Usuario.objects.filter(email=getattr(request.user, 'email', None)).first()
        except Exception:
            usuario = None
        serializer.save(usuario=usuario)


@require_POST
def crear_reseña(request, pk):
    """Vista sencilla para recibir POST desde formulario HTML y crear una reseña."""
    producto = get_object_or_404(Producto, pk=pk)
    puntuacion = request.POST.get('puntuacion')
    comentario = request.POST.get('comentario', '').strip()

    try:
        puntuacion_i = int(puntuacion)
        if puntuacion_i < 1 or puntuacion_i > 5:
            raise ValueError
    except Exception:
        messages.error(request, 'Puntuación inválida. Debe ser entre 1 y 5.')
        return redirect(reverse('producto:detalle', args=[pk]))

    usuario = None
    if request.user and request.user.is_authenticated:
        usuario = Usuario.objects.filter(email=getattr(request.user, 'email', None)).first()

    Resena.objects.create(producto=producto, usuario=usuario, puntuacion=puntuacion_i, comentario=comentario)
    messages.success(request, 'Gracias por tu reseña.')
    return redirect(reverse('producto:detalle', args=[pk]))
from django.shortcuts import render

# Create your views here.
