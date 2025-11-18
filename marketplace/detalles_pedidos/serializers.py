from rest_framework import serializers
from .models import DetalleOrden
from producto.models import Producto


class DetalleOrdenSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.SerializerMethodField(read_only=True)
    producto_precio = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = DetalleOrden
        fields = ['id', 'carrito', 'producto', 'producto_nombre', 'producto_precio', 'cantidad', 'subtotal']
        read_only_fields = ['id', 'subtotal', 'producto_nombre', 'producto_precio']

    def get_producto_nombre(self, obj):
        return getattr(obj.producto, 'nomb_prod', None)

    def get_producto_precio(self, obj):
        return getattr(obj.producto, 'precio', None)

    def validate_cantidad(self, value):
        if value <= 0:
            raise serializers.ValidationError('La cantidad debe ser mayor a cero.')
        return value

    def validate(self, attrs):
        producto = attrs.get('producto') or getattr(self.instance, 'producto', None)
        cantidad = attrs.get('cantidad') or getattr(self.instance, 'cantidad', None)
        if producto and cantidad and producto.stock < cantidad:
            raise serializers.ValidationError('No hay suficiente stock para el producto solicitado.')
        return super().validate(attrs)

    def create(self, validated_data):
        detalle = DetalleOrden.objects.create(**validated_data)
        return detalle

    def update(self, instance, validated_data):
        for k, v in validated_data.items():
            setattr(instance, k, v)
        # subtotal se calcula en save del modelo
        instance.save()
        return instance
