from django.db import models
from django.utils import timezone
from pago.models import MetodoPago
from producto.models import Producto, Categoria
from marketplace.utils.softdelete import SoftDeleteModel
from django.core.files.storage import default_storage
from django.conf import settings


class Promocion(SoftDeleteModel):
    productos = models.ManyToManyField(
        Producto,
        related_name='promociones',
        blank=True,
        verbose_name="Productos aplicados"
    )
    categorias = models.ManyToManyField(
        Categoria,
        related_name='promociones',
        blank=True,
        verbose_name="Categorías aplicadas"
    )
    descripcion = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Descripción"
    )
    descuento_porcentaje = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Descuento (%)",
        help_text="Porcentaje de descuento (ejemplo: 10.00 = 10%)"
    )
    fecha_inicio = models.DateTimeField(verbose_name="Inicio de promoción")
    fecha_fin = models.DateTimeField(verbose_name="Fin de promoción")

    metodo_pago = models.ForeignKey(
        MetodoPago,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='promociones',
        verbose_name="Método de pago"
    )
    imagen_promocion = models.ImageField(
        upload_to='promociones_imagenes/',
        null=True,
        blank=True,
        default='promociones_imagenes/default.png',
        verbose_name="Imagen de promoción"
    )

    class Meta:
        verbose_name = "Promoción"
        verbose_name_plural = "Promociones"
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f"Promoción {self.descripcion or ''} ({self.descuento_porcentaje}%)"

    # --- PROPERTIES Y MÉTODOS ÚTILES ---
    @property
    def activa(self):
        """Indica si la promoción está actualmente activa."""
        ahora = timezone.now()
        return self.fecha_inicio <= ahora <= self.fecha_fin

    @property
    def dias_restantes(self):
        """Devuelve los días restantes para que finalice la promoción."""
        if self.fecha_fin < timezone.now():
            return 0
        return (self.fecha_fin - timezone.now()).days

    @property
    def imagen_url(self):
        """Devuelve la URL de la imagen o una por defecto."""
        # Verificar existencia en storage antes de exponer .url
        if self.imagen_promocion and getattr(self.imagen_promocion, 'name', None):
            try:
                if default_storage.exists(self.imagen_promocion.name):
                    return self.imagen_promocion.url
            except Exception:
                pass
        return settings.MEDIA_URL.rstrip('/') + '/promociones_imagenes/default.png'

    def clean(self):
        """Validación: la fecha de fin debe ser posterior a la de inicio."""
        from django.core.exceptions import ValidationError
        if self.fecha_fin <= self.fecha_inicio:
            raise ValidationError("La fecha de fin debe ser posterior a la fecha de inicio.")

    def descuento_decimal(self):
        """Devuelve el descuento en formato decimal (0.1 en lugar de 10%)."""
        return self.descuento_porcentaje / 100

    def productos_afectados(self):
        """Retorna una lista de los nombres de productos aplicables."""
        return [p.nombre_producto for p in self.productos.all()]

    def categorias_afectadas(self):
        """Retorna una lista de las categorías afectadas."""
        return [c.nombre_categoria for c in self.categorias.all()]
