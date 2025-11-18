from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction
from .models import Carrito
from .serializers import CarritoSerializer

class CarritoViewSet(viewsets.ModelViewSet):
    queryset = Carrito.objects.filter(is_active=True)
    serializer_class = CarritoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        with transaction.atomic():
            serializer.save()

    def perform_update(self, serializer):
        with transaction.atomic():
            serializer.save()

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.is_active = False
            instance.save()

    @action(detail=True, methods=['post'], url_path='restore')
    def restore(self, request, pk=None):
        carrito = self.get_object()
        carrito.is_active = True
        carrito.save()
        return Response({'status': 'restaurado'})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['links'] = {
            'self': request.build_absolute_uri(),
            'update': request.build_absolute_uri(),
            'delete': request.build_absolute_uri(),
            'restore': request.build_absolute_uri('restore/')
        }
        return Response(data)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        for item in response.data:
            item['links'] = {
                'self': request.build_absolute_uri(f"{item['id']}/"),
                'update': request.build_absolute_uri(f"{item['id']}/"),
                'delete': request.build_absolute_uri(f"{item['id']}/"),
                'restore': request.build_absolute_uri(f"{item['id']}/restore/")
            }
        return response
