from django.db import models
from usuario.models import Usuario

class Carrito(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='carritos',
        verbose_name="Usuario"
    )
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )

    def __str__(self):
        return f"Carrito de {self.usuario.username if self.usuario else 'Invitado'} - {self.fecha_creacion.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name = "Carrito"
        verbose_name_plural = "Carritos"
        ordering = ['-fecha_creacion']

    @property
    def total_items(self):
        """
        Devuelve la cantidad total de productos en el carrito (si existe un modelo DetalleCarrito o similar).
        """
        return getattr(self, 'detalles', []).count() if hasattr(self, 'detalles') else 0
