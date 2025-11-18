from rest_framework import serializers
from .models import Orden
from carrito.serializers import CarritoSerializer


class OrdenSerializer(serializers.ModelSerializer):
    carrito = CarritoSerializer(read_only=True)
    from carrito.models import Carrito
    carrito_id = serializers.PrimaryKeyRelatedField(write_only=True, source='carrito', queryset=Carrito.objects.all())
    entregada = serializers.SerializerMethodField()
    pendiente = serializers.SerializerMethodField()

    class Meta:
        model = Orden
        fields = [
            'id', 'carrito', 'carrito_id', 'total', 'direccion_entrega', 'distrito_entrega',
            'provincia_entrega', 'pais_entrega', 'fecha_envio', 'fecha_entrega', 'estado',
            'fecha_creacion', 'entregada', 'pendiente'
        ]
        read_only_fields = ['id', 'fecha_creacion', 'entregada', 'pendiente']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from carrito.models import Carrito
        self.fields['carrito_id'].queryset = Carrito.objects.all()

    def get_entregada(self, obj):
        return obj.entregada

    def get_pendiente(self, obj):
        return obj.pendiente

    def validate(self, attrs):
        # calcular total a partir del carrito si se proporciona
        carrito = attrs.get('carrito') or getattr(self.instance, 'carrito', None)
        if carrito and hasattr(carrito, 'detalles'):
            total = sum(d.subtotal for d in carrito.detalles.all())
            attrs['total'] = total
        return super().validate(attrs)
