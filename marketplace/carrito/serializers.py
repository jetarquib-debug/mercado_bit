from rest_framework import serializers
from .models import Carrito


class CarritoSerializer(serializers.ModelSerializer):
    total_items = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Carrito
        fields = ['id', 'usuario', 'fecha_creacion', 'total_items']
        read_only_fields = ['id', 'fecha_creacion', 'total_items']

    def get_total_items(self, obj):
        try:
            return obj.detalles.count()
        except Exception:
            return 0
