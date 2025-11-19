from rest_framework import serializers
from .models import DetalleOrden
from producto.serializers import ProductoSerializer


class DetalleOrdenSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True)
    producto_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=(), source='producto')
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = DetalleOrden
        fields = ['id', 'carrito', 'producto', 'producto_id', 'cantidad', 'subtotal']
        read_only_fields = ['id', 'subtotal']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # evitar import circular
        from producto.models import Producto
        self.fields['producto_id'].queryset = Producto.objects.all()

    def validate_cantidad(self, value):
        if value <= 0:
            raise serializers.ValidationError('La cantidad debe ser mayor que cero.')
        return value

    def create(self, validated_data):
        detalle = super().create(validated_data)
        # subtotal se calcula en save() del modelo
        detalle.refresh_from_db()
        return detalle

    def validate(self, data):
        # Validación cruzada: cantidad vs stock del producto
        producto = data.get('producto')
        cantidad = data.get('cantidad')
        if producto and cantidad is not None:
            if cantidad <= 0:
                raise serializers.ValidationError({'cantidad': 'La cantidad debe ser mayor que cero.'})
            if cantidad > producto.stock:
                raise serializers.ValidationError({'cantidad': 'Cantidad solicitada supera stock disponible.'})
        return data
