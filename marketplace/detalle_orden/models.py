from django.db import models
from carrito.models import Carrito
from usuario.models import Pais, Provincia, Distrito

class Orden(models.Model):
    ESTADO_CHOICES = [
        ('pendiente_envio', 'Pendiente de Envío'),
        ('preparando_envio', 'Preparando Envío'),
        ('en_transito', 'En Tránsito'),
        ('en_reparto', 'En Reparto'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]

    carrito = models.ForeignKey(
        Carrito,
        on_delete=models.CASCADE,
        related_name='ordenes',
        verbose_name="Carrito asociado"
    )
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total (S/.)")

    direccion_entrega = models.CharField(max_length=200, null=True, blank=True, verbose_name="Dirección de entrega")
    distrito_entrega = models.ForeignKey(Distrito, null=True, blank=True, on_delete=models.SET_NULL, related_name='ordenes', verbose_name="Distrito")
    provincia_entrega = models.ForeignKey(Provincia, null=True, blank=True, on_delete=models.SET_NULL, related_name='ordenes', verbose_name="Provincia")
    pais_entrega = models.ForeignKey(Pais, null=True, blank=True, on_delete=models.SET_NULL, related_name='ordenes', verbose_name="País")

    fecha_envio = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de envío")
    fecha_entrega = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de entrega")
    estado = models.CharField(max_length=30, choices=ESTADO_CHOICES, default='pendiente_envio', verbose_name="Estado")

    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        verbose_name = "Orden"
        verbose_name_plural = "Órdenes"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Orden #{self.id} - {self.get_estado_display()} (S/. {self.total:.2f})"

    def calcular_total(self):
        """
        Recalcula el total sumando los subtotales de los detalles del carrito.
        """
        if self.carrito and hasattr(self.carrito, 'detalles'):
            detalles = self.carrito.detalles.all()
            self.total = sum(detalle.subtotal for detalle in detalles)
            self.save()
        return self.total

    @property
    def entregada(self):
        """Retorna True si la orden ya fue entregada."""
        return self.estado == 'entregado'

    @property
    def pendiente(self):
        """Retorna True si la orden aún no ha sido enviada."""
        return self.estado == 'pendiente_envio'
