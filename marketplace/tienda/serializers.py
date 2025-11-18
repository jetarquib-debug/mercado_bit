from rest_framework import serializers
from .models import Tienda, ImagenPerfilTienda
from usuario.serializers import UsuarioSerializer
from usuario.models import Usuario


class ImagenPerfilTiendaSerializer(serializers.ModelSerializer):
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = ImagenPerfilTienda
        fields = ['id', 'imagen', 'imagen_url', 'fecha_subida', 'es_principal']
        read_only_fields = ['id', 'imagen_url', 'fecha_subida']

    def get_imagen_url(self, obj):
        try:
            return obj.imagen.url
        except Exception:
            return None


class TiendaSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    usuario_id = serializers.PrimaryKeyRelatedField(write_only=True, source='usuario', queryset=Usuario.objects.all())
    imagenes = ImagenPerfilTiendaSerializer(many=True, read_only=True)
    imagen_principal = serializers.SerializerMethodField()
    ubicacion_completa = serializers.SerializerMethodField()
    telefono_formateado = serializers.SerializerMethodField()

    class Meta:
        model = Tienda
        fields = [
            'id', 'nombre_tienda', 'descripcion', 'email', 'codigo_pais', 'telefono', 'direccion',
            'distrito', 'provincia', 'departamento', 'pais', 'fecha_registro', 'ruc', 'usuario', 'usuario_id',
            'imagenes', 'imagen_principal', 'ubicacion_completa', 'telefono_formateado'
        ]
        read_only_fields = ['id', 'fecha_registro', 'imagen_principal', 'ubicacion_completa', 'telefono_formateado']


    def get_imagen_principal(self, obj):
        try:
            return obj.imagen_principal
        except Exception:
            return None

    def get_ubicacion_completa(self, obj):
        return obj.ubicacion_completa

    def get_telefono_formateado(self, obj):
        return obj.telefono_formateado

    def validate_ruc(self, value):
        if value and len(value) not in (11,):
            raise serializers.ValidationError('El RUC debe tener 11 caracteres.')
        return value
