from rest_framework import serializers
from .models import Promocion
from producto.serializers import ProductoSerializer, CategoriaSerializer


class PromocionSerializer(serializers.ModelSerializer):
    productos = serializers.PrimaryKeyRelatedField(many=True, queryset=(), required=False)
    categorias = serializers.PrimaryKeyRelatedField(many=True, queryset=(), required=False)
    activa = serializers.SerializerMethodField(read_only=True)
    dias_restantes = serializers.SerializerMethodField(read_only=True)
    imagen_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Promocion
        fields = ['id', 'productos', 'categorias', 'descripcion', 'descuento_porcentaje', 'fecha_inicio', 'fecha_fin',
                  'metodo_pago', 'imagen_promocion', 'activa', 'dias_restantes', 'imagen_url']
        read_only_fields = ['id', 'activa', 'dias_restantes', 'imagen_url']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # asignar queryset evitando import circular
        from producto.models import Producto, Categoria
        self.fields['productos'].queryset = Producto.objects.all()
        self.fields['categorias'].queryset = Categoria.objects.all()

    def get_activa(self, obj):
        return obj.activa

    def get_dias_restantes(self, obj):
        return obj.dias_restantes

    def get_imagen_url(self, obj):
        return obj.imagen_url

    def validate(self, data):
        if 'fecha_fin' in data and 'fecha_inicio' in data and data['fecha_fin'] <= data['fecha_inicio']:
            raise serializers.ValidationError('La fecha de fin debe ser posterior a la fecha de inicio.')
        return data
