from rest_framework import serializers
from .models import Promocion
from producto.models import Producto, Categoria


class PromocionSerializer(serializers.ModelSerializer):
    productos_ids = serializers.PrimaryKeyRelatedField(many=True, write_only=True, source='productos', queryset=Producto.objects.all(), required=False)
    categorias_ids = serializers.PrimaryKeyRelatedField(many=True, write_only=True, source='categorias', queryset=Categoria.objects.all(), required=False)
    activa = serializers.SerializerMethodField()
    dias_restantes = serializers.SerializerMethodField()
    imagen_url = serializers.SerializerMethodField()
    descuento_decimal = serializers.SerializerMethodField()

    class Meta:
        model = Promocion
        fields = [
            'id', 'productos', 'productos_ids', 'categorias', 'categorias_ids', 'descripcion',
            'descuento_porcentaje', 'fecha_inicio', 'fecha_fin', 'metodo_pago', 'imagen_promocion',
            'activa', 'dias_restantes', 'imagen_url', 'descuento_decimal'
        ]
        read_only_fields = ['id', 'productos', 'categorias', 'activa', 'dias_restantes', 'imagen_url', 'descuento_decimal']

    def get_activa(self, obj):
        return obj.activa

    def get_dias_restantes(self, obj):
        return obj.dias_restantes

    def get_imagen_url(self, obj):
        try:
            return obj.imagen_promocion.url
        except Exception:
            return None

    def get_descuento_decimal(self, obj):
        try:
            return float(obj.descuento_porcentaje) / 100.0
        except Exception:
            return None

    def validate(self, attrs):
        inicio = attrs.get('fecha_inicio') or getattr(self.instance, 'fecha_inicio', None)
        fin = attrs.get('fecha_fin') or getattr(self.instance, 'fecha_fin', None)
        if inicio and fin and fin <= inicio:
            raise serializers.ValidationError('La fecha de fin debe ser posterior a la fecha de inicio.')
        return super().validate(attrs)

    def create(self, validated_data):
        productos = validated_data.pop('productos', [])
        categorias = validated_data.pop('categorias', [])
        promo = Promocion.objects.create(**validated_data)
        if productos:
            promo.productos.set(productos)
        if categorias:
            promo.categorias.set(categorias)
        return promo

    def update(self, instance, validated_data):
        productos = validated_data.pop('productos', None)
        categorias = validated_data.pop('categorias', None)
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        if productos is not None:
            instance.productos.set(productos)
        if categorias is not None:
            instance.categorias.set(categorias)
        return instance
