from rest_framework import serializers
from .models import Tienda, ImagenPerfilTienda


class ImagenPerfilTiendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenPerfilTienda
        fields = ['id', 'imagen', 'fecha_subida', 'es_principal']
        read_only_fields = ['id', 'fecha_subida']


class TiendaSerializer(serializers.ModelSerializer):
    imagenes = ImagenPerfilTiendaSerializer(many=True, read_only=True)
    ubicacion_completa = serializers.SerializerMethodField(read_only=True)
    telefono_formateado = serializers.SerializerMethodField(read_only=True)
    imagen_principal = serializers.SerializerMethodField(read_only=True)
    usuario = serializers.PrimaryKeyRelatedField(queryset=())

    class Meta:
        model = Tienda
        fields = ['id', 'nombre_tienda', 'descripcion', 'email', 'telefono', 'direccion',
                  'distrito', 'provincia', 'departamento', 'pais', 'fecha_registro', 'ruc', 'usuario',
                  'imagenes', 'ubicacion_completa', 'telefono_formateado', 'imagen_principal']
        read_only_fields = ['id', 'fecha_registro', 'ubicacion_completa', 'telefono_formateado', 'imagen_principal']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # evitar import circular: asignar queryset a runtime
        from usuario.models import Usuario
        self.fields['usuario'].queryset = Usuario.objects.all()

    def get_ubicacion_completa(self, obj):
        return obj.ubicacion_completa

    def get_telefono_formateado(self, obj):
        return obj.telefono_formateado

    def get_imagen_principal(self, obj):
        try:
            return obj.imagen_principal
        except Exception:
            return None

    def validate_email(self, value):
        # asegúrate de que el email sea válido y único (modelo ya impone unique)
        if value and '@' not in value:
            raise serializers.ValidationError('Correo inválido.')
        return value
