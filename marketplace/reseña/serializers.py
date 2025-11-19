from rest_framework import serializers
from .models import Resena


class ResenaSerializer(serializers.ModelSerializer):
    usuario_email = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Resena
        fields = ['id', 'producto', 'usuario', 'usuario_email', 'puntuacion', 'comentario', 'fecha_creacion']
        read_only_fields = ['id', 'fecha_creacion', 'usuario']

    def validate_puntuacion(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError('La puntuación debe estar entre 1 y 5.')
        return value

    def get_usuario_email(self, obj):
        try:
            return obj.usuario.email if obj.usuario else None
        except Exception:
            return None
