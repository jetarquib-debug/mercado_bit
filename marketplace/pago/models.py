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


# 💳 Pagos
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
        blank=True,
        null=True,
        related_name='pagos',
        verbose_name="Método de pago"
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente',
        verbose_name="Estado del pago"
    )
    fecha_pago = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de pago")
    monto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Monto pagado (S/.)"
    )

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        ordering = ['-fecha_pago']

    def __str__(self):
        return f"Pago #{self.id} - {self.get_estado_display()} - Orden #{self.orden.id if self.orden else 'N/A'}"

    @property
    def es_exitoso(self):
        """True si el pago fue completado."""
        return self.estado == 'completado'

    def procesar_pago(self, monto=None):
        """
        Procesa el pago (ejemplo para integración futura con APIs de pago).
        """
        if monto:
            self.monto = monto
        if self.estado == 'pendiente':
            self.estado = 'procesando'
        self.save()
        return self.estado
