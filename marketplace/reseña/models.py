from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from producto.models import Producto
from usuario.models import Usuario
from marketplace.utils.softdelete import SoftDeleteModel


class Resena(SoftDeleteModel):
	producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='resenas')
	usuario = models.ForeignKey(Usuario, null=True, blank=True, on_delete=models.SET_NULL, related_name='resenas')
	puntuacion = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
	comentario = models.TextField(null=True, blank=True)
	fecha_creacion = models.DateTimeField(default=timezone.now)

	class Meta:
		verbose_name = 'Reseña'
		verbose_name_plural = 'Reseñas'
		ordering = ['-fecha_creacion']

	def __str__(self):
		user = self.usuario.email if self.usuario else 'Anónimo'
		return f"Reseña {self.pk} - {user} - {self.producto.nomb_prod} ({self.puntuacion})"
