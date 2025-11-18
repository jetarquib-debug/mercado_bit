from rest_framework import serializers
from .models import Marca, Categoria, Producto, ImagenProducto


class MarcaSerializer(serializers.ModelSerializer):
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = Marca
        fields = ['id', 'nomb_marca', 'imagen_url']
        read_only_fields = ['id', 'imagen_url']

    def get_imagen_url(self, obj):
        try:
            return obj.imagen_marca.url
        except Exception:
            return None


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nomb_ca', 'descripcion']
        read_only_fields = ['id']


class ImagenProductoSerializer(serializers.ModelSerializer):
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = ImagenProducto
        fields = ['id', 'imagen', 'imagen_url', 'es_principal', 'fecha_subida']
        read_only_fields = ['id', 'imagen_url', 'fecha_subida']

    def get_imagen_url(self, obj):
        try:
            return obj.imagen.url
        except Exception:
            return None


class ProductoSerializer(serializers.ModelSerializer):
    def delete(self, instance):
        instance.is_active = False
        instance.save()
        return instance
    marca = MarcaSerializer(read_only=True)
    marca_id = serializers.PrimaryKeyRelatedField(
        queryset=Marca.objects.all(), source='marca', write_only=True, required=False, allow_null=True
    )
    categorias = CategoriaSerializer(many=True, read_only=True)
    categorias_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Categoria.objects.all(), source='categoria', write_only=True, required=False
    )
    imagenes = ImagenProductoSerializer(many=True, read_only=True)

    disponible = serializers.SerializerMethodField()
    imagen_principal_url = serializers.SerializerMethodField()
    cantidad_imagenes = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = [
            'id', 'tienda', 'nomb_prod', 'descripcion', 'precio', 'stock', 'fecha_creacion', 'peso', 'estado',
            'marca', 'marca_id', 'categorias', 'categorias_ids', 'imagenes',
            'disponible', 'imagen_principal_url', 'cantidad_imagenes'
        ]
        read_only_fields = ['id', 'fecha_creacion', 'disponible', 'imagen_principal_url', 'cantidad_imagenes']

    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError('El precio debe ser mayor a cero.')
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError('El stock no puede ser negativo.')
        return value

    def get_disponible(self, obj):
        return obj.disponible

    def get_imagen_principal_url(self, obj):
        try:
            return obj.imagen_principal_url
        except Exception:
            return None

    def get_cantidad_imagenes(self, obj):
        return obj.imagenes.count()

    def create(self, validated_data):
        categorias = validated_data.pop('categoria', []) if 'categoria' in validated_data else []
        producto = Producto.objects.create(**validated_data)
        if categorias:
            producto.categoria.set(categorias)
        return producto

    def update(self, instance, validated_data):
        categorias = validated_data.pop('categoria', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if categorias is not None:
            instance.categoria.set(categorias)
        return instance
