from rest_framework import serializers
from .models import Carrito
from detalles_pedidos.serializers import DetalleOrdenSerializer


class CarritoSerializer(serializers.ModelSerializer):
    detalles = DetalleOrdenSerializer(many=True, read_only=True)
    total_items = serializers.SerializerMethodField(read_only=True)
    total_amount = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Carrito
        fields = ['id', 'usuario', 'fecha_creacion', 'detalles', 'total_items', 'total_amount']
        read_only_fields = ['id', 'fecha_creacion', 'detalles', 'total_items', 'total_amount']

    def get_total_items(self, obj):
        return obj.total_items if hasattr(obj, 'total_items') else obj.detalles.count() if hasattr(obj, 'detalles') else 0

    def get_total_amount(self, obj):
        if hasattr(obj, 'detalles'):
            return sum([d.subtotal for d in obj.detalles.all()])
        return 0
