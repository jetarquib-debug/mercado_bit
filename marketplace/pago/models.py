from django.db import models
from detalle_orden.models import Orden

# 🏦 Métodos de pago
class MetodoPago(models.Model):
    nomb_meto = models.CharField(max_length=50, unique=True, verbose_name="Nombre del método")
    imagen_metodo = models.ImageField(
        upload_to='metodos_pago_imagenes/',
        null=True,
        blank=True,
        default='metodos_pago_imagenes/default.png',
        verbose_name="Imagen del método"
    )

    class Meta:
        verbose_name = "Método de Pago"
        verbose_name_plural = "Métodos de Pago"
        ordering = ['nomb_meto']

    def __str__(self):
        return self.nomb_meto

    @property
    def imagen_url(self):
        """Devuelve la URL completa de la imagen o la ruta por defecto."""
        try:
            return self.imagen_metodo.url
        except ValueError:
            return '/media/metodos_pago_imagenes/default.png'

# 💳 Modelo: Pagos
class Pago(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('procesando', 'Procesando'),
        ('completado', 'Completado'),
        ('fallido', 'Fallido'),
        ('reembolsado', 'Reembolsado'),
        ('cancelado', 'Cancelado'),
    ]

    orden = models.ForeignKey(
        Orden,
        on_delete=models.CASCADE,
        related_name='pagos',
        verbose_name="Orden asociada"
    )
    metodo = models.ForeignKey(
        MetodoPago,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pagos',
        verbose_name="Método de pago"
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente',
        verbose_name="Estado del pago"
    )
    monto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Monto pagado (S/.)"
    )
    fecha_pago = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de pago"
    )
    actualizado_en = models.DateTimeField(
        auto_now=True,
        verbose_name="Actualizado en"
    )
    transaccion_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        unique=True,
        verbose_name="ID de transacción (referencia externa)"
    )
    notas = models.TextField(
        blank=True,
        null=True,
        verbose_name="Notas adicionales"
    )

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        ordering = ['-fecha_pago']

    def __str__(self):
        return f"Pago #{self.id or '—'} | {self.get_estado_display()} | Orden #{self.orden.id if self.orden else 'N/A'}"

    # --- PROPIEDADES ÚTILES ---
    @property
    def es_exitoso(self):
        """Retorna True si el pago fue completado exitosamente."""
        return self.estado == 'completado'

    @property
    def es_fallido(self):
        """Retorna True si el pago falló o fue cancelado."""
        return self.estado in ['fallido', 'cancelado']

    # --- MÉTODOS DE NEGOCIO ---
    def procesar_pago(self, monto=None):
        """
        Simula el procesamiento de un pago.
        En una integración real, aquí se conectaría con una pasarela externa.
        """
        if monto is not None:
            self.monto = monto

        if self.estado == 'pendiente':
            self.estado = 'procesando'
            self.save(update_fields=['estado', 'monto', 'actualizado_en'])
        return self.estado

    def completar_pago(self, transaccion_id=None):
        """
        Marca el pago como completado exitosamente.
        """
        self.estado = 'completado'
        self.fecha_pago = models.DateTimeField(auto_now_add=True)
        if transaccion_id:
            self.transaccion_id = transaccion_id
        self.save(update_fields=['estado', 'fecha_pago', 'transaccion_id', 'actualizado_en'])
        return self.estado

    def marcar_fallido(self, motivo=None):
        """
        Marca el pago como fallido y agrega una nota opcional.
        """
        self.estado = 'fallido'
        if motivo:
            self.notas = f"❌ Pago fallido: {motivo}"
        self.save(update_fields=['estado', 'notas', 'actualizado_en'])
        return self.estado

    def reembolsar(self):
        """Marca el pago como reembolsado."""
        self.estado = 'reembolsado'
        self.save(update_fields=['estado', 'actualizado_en'])
        return self.estado
