from rest_framework import serializers
from .models import Producto, Marca, Categoria, ImagenProducto
from promociones.models import Promocion


class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ['id', 'nomb_marca', 'imagen_marca']
        read_only_fields = ['id']


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nomb_ca', 'descripcion']
        read_only_fields = ['id']


class ImagenProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenProducto
        fields = ['id', 'imagen', 'es_principal', 'fecha_subida']
        read_only_fields = ['id', 'fecha_subida']


class ProductoSerializer(serializers.ModelSerializer):
    marca = MarcaSerializer(required=False, allow_null=True)
    categoria = CategoriaSerializer(many=True, read_only=True)
    imagenes = ImagenProductoSerializer(many=True, read_only=True)

    disponible = serializers.SerializerMethodField(read_only=True)
    imagen_principal_url = serializers.SerializerMethodField(read_only=True)
    precio_final = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Producto
        fields = [
            'id', 'tienda', 'nomb_prod', 'descripcion', 'precio', 'stock', 'fecha_creacion',
            'peso', 'estado', 'marca', 'categoria', 'imagenes', 'disponible', 'imagen_principal_url', 'precio_final'
        ]
        read_only_fields = ['id', 'fecha_creacion', 'disponible', 'imagen_principal_url', 'precio_final']

    def get_disponible(self, obj):
        return obj.disponible

    def get_imagen_principal_url(self, obj):
        try:
            return obj.imagen_principal_url
        except Exception:
            return None

    def get_precio_final(self, obj):
        """Aplica la mejor promoción activa (si existe) y devuelve el precio final."""
        try:
            promociones = Promocion.objects.filter(fecha_inicio__lte=serializers.datetime.datetime.now(), fecha_fin__gte=serializers.datetime.datetime.now())
        except Exception:
            promociones = Promocion.objects.none()

        max_desc = 0
        for p in promociones:
            if obj in p.productos.all():
                try:
                    val = float(p.descuento_porcentaje)
                except Exception:
                    val = 0
                if val > max_desc:
                    max_desc = val
            else:
                # revisar categorías
                prod_cats = set(obj.categoria.all())
                promo_cats = set(p.categorias.all())
                if prod_cats & promo_cats:
                    try:
                        val = float(p.descuento_porcentaje)
                    except Exception:
                        val = 0
                    if val > max_desc:
                        max_desc = val

        if max_desc <= 0:
            return obj.precio
        descuento = (obj.precio * max_desc) / 100
        return obj.precio - descuento

    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor a cero.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo.")
        return value

    def create(self, validated_data):
        # permitir que la marca venga como dict o id
        marca_data = validated_data.pop('marca', None)
        if isinstance(marca_data, dict):
            marca_obj, _ = Marca.objects.get_or_create(**marca_data)
            validated_data['marca'] = marca_obj
        return super().create(validated_data)
