from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Usuario, ImagenPerfilUsuario, Pais, Departamento, Provincia, Distrito, CodigoPais


class ImagenPerfilUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenPerfilUsuario
        fields = ['id', 'imagen', 'fecha_subida', 'es_principal']
        read_only_fields = ['id', 'fecha_subida']


class UsuarioSerializer(serializers.ModelSerializer):
    imagenes = ImagenPerfilUsuarioSerializer(many=True, read_only=True)
    imagen_principal = serializers.SerializerMethodField(read_only=True)
    contrasena = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Usuario
        fields = ['id', 'nombres', 'apellidos', 'email', 'contrasena', 'imagenes', 'imagen_principal',
                  'codigo_pais', 'telefono', 'direccion', 'pais', 'departamento', 'provincia', 'distrito',
                  'sexo', 'fecha_registro', 'dni_ce']
        read_only_fields = ['id', 'imagen_principal', 'fecha_registro']

    def get_imagen_principal(self, obj):
        try:
            return obj.imagen_principal
        except Exception:
            return None

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError('El email es requerido')
        return value

    def create(self, validated_data):
        pwd = validated_data.pop('contrasena')
        validated_data['contrasena'] = make_password(pwd)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        pwd = validated_data.pop('contrasena', None)
        if pwd:
            instance.contrasena = make_password(pwd)
        return super().update(instance, validated_data)


class UsuarioSerializerMinimal(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombres', 'apellidos', 'email']
        read_only_fields = ['id']
