from django.db import models
from carrito.models import Carrito
from producto.models import Producto
from marketplace.utils.softdelete import SoftDeleteModel


class DetalleOrden(SoftDeleteModel):
    carrito = models.ForeignKey(
        Carrito,
        on_delete=models.CASCADE,
        related_name='detalles',
        verbose_name="Carrito"
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='detalles_orden',
        verbose_name="Producto"
    )
    cantidad = models.PositiveIntegerField(default=1, verbose_name="Cantidad")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False, verbose_name="Subtotal")

    def save(self, *args, **kwargs):
        # Calcular subtotal automáticamente
        self.subtotal = self.producto.precio * self.cantidad
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad} × {self.producto.nomb_prod} (Carrito #{self.carrito.id})"

    class Meta:
        verbose_name = "Detalle de Orden"
        verbose_name_plural = "Detalles de Órdenes"
        ordering = ['carrito']

    def delete(self, using=None, keep_parents=False):
        # soft delete detalle
        self.soft_delete()
