from rest_framework import serializers
from .models import Orden
from carrito.serializers import CarritoSerializer


class OrdenSerializer(serializers.ModelSerializer):
    carrito = CarritoSerializer(read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    entregada = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Orden
        fields = ['id', 'carrito', 'total', 'direccion_entrega', 'distrito_entrega', 'provincia_entrega', 'pais_entrega',
                  'fecha_envio', 'fecha_entrega', 'estado', 'fecha_creacion', 'entregada']
        read_only_fields = ['id', 'total', 'fecha_creacion', 'entregada']

    def get_entregada(self, obj):
        return obj.entregada

    def validate(self, data):
        # si total es proporcionado por cliente, verificar que sea consistente
        return data
