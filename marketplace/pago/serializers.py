from rest_framework import serializers
from .models import MetodoPago, Pago
from detalle_orden.serializers import OrdenSerializer


class MetodoPagoSerializer(serializers.ModelSerializer):
    imagen_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MetodoPago
        fields = ['id', 'nomb_meto', 'imagen_metodo', 'imagen_url']
        read_only_fields = ['id', 'imagen_url']

    def get_imagen_url(self, obj):
        try:
            return obj.imagen_url
        except Exception:
            return None


class PagoSerializer(serializers.ModelSerializer):
    orden = serializers.PrimaryKeyRelatedField(queryset=())
    metodo = serializers.PrimaryKeyRelatedField(queryset=(), allow_null=True, required=False)
    es_exitoso = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Pago
        fields = ['id', 'orden', 'metodo', 'estado', 'monto', 'fecha_pago', 'actualizado_en', 'transaccion_id', 'notas', 'es_exitoso']
        read_only_fields = ['id', 'fecha_pago', 'actualizado_en', 'es_exitoso']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from detalle_orden.models import Orden
        from pago.models import MetodoPago
        self.fields['orden'].queryset = Orden.objects.all()
        self.fields['metodo'].queryset = MetodoPago.objects.all()

    def get_es_exitoso(self, obj):
        return obj.es_exitoso

    def validate_monto(self, value):
        if value < 0:
            raise serializers.ValidationError('El monto no puede ser negativo.')
        return value
