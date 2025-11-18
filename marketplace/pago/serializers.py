from rest_framework import serializers
from .models import MetodoPago, Pago


class MetodoPagoSerializer(serializers.ModelSerializer):
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = MetodoPago
        fields = ['id', 'nomb_meto', 'imagen_metodo', 'imagen_url']
        read_only_fields = ['id', 'imagen_url']

    def get_imagen_url(self, obj):
        try:
            return obj.imagen_metodo.url
        except Exception:
            return None


class PagoSerializer(serializers.ModelSerializer):
    metodo = MetodoPagoSerializer(read_only=True)
    metodo_id = serializers.PrimaryKeyRelatedField(write_only=True, source='metodo', queryset=MetodoPago.objects.all(), required=False, allow_null=True)
    es_exitoso = serializers.SerializerMethodField()

    class Meta:
        model = Pago
        fields = ['id', 'orden', 'metodo', 'metodo_id', 'estado', 'monto', 'fecha_pago', 'transaccion_id', 'notas', 'es_exitoso']
        read_only_fields = ['id', 'fecha_pago', 'es_exitoso']

    def get_es_exitoso(self, obj):
        return obj.es_exitoso

    def validate_monto(self, value):
        if value < 0:
            raise serializers.ValidationError('El monto no puede ser negativo.')
        return value
