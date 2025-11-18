from rest_framework import serializers
from .models import (
    ImagenPerfilUsuario, Pais, Departamento, Provincia, Distrito, CodigoPais, Usuario
)


class ImagenPerfilUsuarioSerializer(serializers.ModelSerializer):
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = ImagenPerfilUsuario
        fields = ['id', 'imagen', 'imagen_url', 'fecha_subida', 'es_principal']
        read_only_fields = ['id', 'imagen_url', 'fecha_subida']

    def get_imagen_url(self, obj):
        try:
            return obj.imagen.url
        except Exception:
            return None


class CodigoPaisSerializer(serializers.ModelSerializer):
    pais_nombre = serializers.CharField(source='pais.nomb_pais', read_only=True)

    class Meta:
        model = CodigoPais
        fields = ['id', 'pais', 'pais_nombre', 'codigo', 'imagen_pais']
        read_only_fields = ['id', 'pais_nombre']


class LocalizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pais
        fields = ['id', 'nomb_pais']
        read_only_fields = ['id']


class UsuarioSerializer(serializers.ModelSerializer):
    imagenes = ImagenPerfilUsuarioSerializer(many=True, read_only=True)
    imagenes_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=ImagenPerfilUsuario.objects.all(), write_only=True, required=False, source='imagenes'
    )
    contrasena = serializers.CharField(write_only=True, required=True)
    imagen_principal = serializers.SerializerMethodField()
    nombre_completo = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = [
            'id', 'nombres', 'apellidos', 'email', 'contrasena', 'imagenes', 'imagenes_ids',
            'codigo_pais', 'telefono', 'direccion', 'pais', 'departamento', 'provincia', 'distrito',
            'sexo', 'fecha_registro', 'dni_ce', 'imagen_principal', 'nombre_completo'
        ]
        read_only_fields = ['id', 'fecha_registro', 'imagen_principal', 'nombre_completo']

    def get_imagen_principal(self, obj):
        try:
            return obj.imagen_principal
        except Exception:
            return None

    def get_nombre_completo(self, obj):
        return f"{obj.nombres or ''} {obj.apellidos or ''}".strip()

    def validate_email(self, value):
        if Usuario.objects.filter(email=value).exclude(pk=getattr(self.instance, 'pk', None)).exists():
            raise serializers.ValidationError('Ya existe un usuario con ese correo.')
        return value

    def create(self, validated_data):
        imagenes = validated_data.pop('imagenes', [])
        usuario = Usuario.objects.create(**validated_data)
        if imagenes:
            usuario.imagenes.set(imagenes)
        return usuario

    def update(self, instance, validated_data):
        imagenes = validated_data.pop('imagenes', None)
        contrasena = validated_data.pop('contrasena', None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        if contrasena:
            instance.contrasena = contrasena
        instance.save()
        if imagenes is not None:
            instance.imagenes.set(imagenes)
        return instance
