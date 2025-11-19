from django.db import models
from django.utils.html import format_html
from django.core.files.storage import default_storage
from django.conf import settings
from tienda.models import Tienda
from usuario.models import Usuario
from marketplace.utils.softdelete import SoftDeleteModel


# ==============================
# 🏷️ MARCA
# ==============================
class Marca(SoftDeleteModel):
    nomb_marca = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la marca")
    imagen_marca = models.ImageField(
        upload_to='marcas_imagenes/',
        null=True, blank=True,
        default='marcas_imagenes/default_marca.png',
        verbose_name="Imagen de la marca"
    )

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"
        ordering = ['nomb_marca']

    def __str__(self):
        return self.nomb_marca

    def vista_previa(self):
        """Muestra vista previa de la imagen en el admin."""
        # Corrección: verificar que el archivo exista en el storage antes de usar .url
        if self.imagen_marca and getattr(self.imagen_marca, 'name', None):
            try:
                if default_storage.exists(self.imagen_marca.name):
                    return format_html(
                        '<img src="{}" width="60" height="60" style="object-fit:cover; border-radius:8px; box-shadow:0 0 3px #888;" />',
                        self.imagen_marca.url
                    )
            except Exception:
                # si storage falla, caer al fallback
                pass
        # fallback: imagen por defecto si el archivo no está presente
        default_url = settings.MEDIA_URL.rstrip('/') + '/marcas_imagenes/default_marca.png'
        return format_html('<img src="{}" width="60" height="60" />', default_url)
        return "(Sin imagen)"
    vista_previa.short_description = "Vista previa"
    vista_previa.allow_tags = True


# ==============================
# 🧩 CATEGORÍA
# ==============================
class Categoria(SoftDeleteModel):
    nomb_ca = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la categoría")
    descripcion = models.CharField(max_length=255, null=True, blank=True, verbose_name="Descripción")
    imagen_categoria = models.ImageField(
        upload_to='categorias_imagenes/',
        null=True, blank=True,
        default='categorias_imagenes/default_categoria.png',
        verbose_name="Imagen de la categoría"
    )

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nomb_ca']

    def __str__(self):
        return self.nomb_ca

    def vista_previa(self):
        """Vista previa de la categoría en admin."""
        # Corrección: verificar existencia del archivo en storage antes de usar .url
        if self.imagen_categoria and getattr(self.imagen_categoria, 'name', None):
            try:
                if default_storage.exists(self.imagen_categoria.name):
                    return format_html(
                        '<img src="{}" width="60" height="60" style="object-fit:cover; border-radius:8px; box-shadow:0 0 3px #888;" />',
                        self.imagen_categoria.url
                    )
            except Exception:
                pass
        default_url = settings.MEDIA_URL.rstrip('/') + '/categorias_imagenes/default_categoria.png'
        return format_html('<img src="{}" width="60" height="60" />', default_url)
        return "(Sin imagen)"
    vista_previa.short_description = "Vista previa"
    vista_previa.allow_tags = True


# ==============================
# 📦 PRODUCTO
# ==============================
class Producto(SoftDeleteModel):
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('agotado', 'Agotado'),
        ('preventa', 'Preventa'),
        ('reacondicionado', 'Reacondicionado'),
        ('descargable', 'Descargable'),
    ]

    tienda = models.ForeignKey(
        Tienda, on_delete=models.CASCADE, related_name='productos', verbose_name="Tienda"
    )
    nomb_prod = models.CharField(max_length=100, verbose_name="Nombre del producto")
    descripcion = models.CharField(max_length=255, null=True, blank=True, verbose_name="Descripción")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio (S/.)")
    stock = models.PositiveIntegerField(verbose_name="Stock disponible")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    peso = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Peso (kg)")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, verbose_name="Estado")

    marca = models.ForeignKey(
        Marca, null=True, on_delete=models.SET_NULL, related_name='productos', verbose_name="Marca"
    )
    categoria = models.ManyToManyField(
        Categoria, related_name='productos', verbose_name="Categorías"
    )

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.nomb_prod} ({self.tienda.nombre_tienda})"

    def clean(self):
        """Validación de datos antes de guardar."""
        from django.core.exceptions import ValidationError
        if self.precio <= 0:
            raise ValidationError("El precio debe ser mayor a cero.")
        if self.stock < 0:
            raise ValidationError("El stock no puede ser negativo.")

    @property
    def disponible(self):
        """Retorna True si el producto tiene stock disponible."""
        return self.estado == 'disponible' and self.stock > 0

    @property
    def imagen_principal_url(self):
        """Devuelve la imagen principal o una por defecto."""
        imagen = self.imagenes.filter(es_principal=True).first()
        # Corrección: asegurar que la ruta exista en el storage antes de acceder a .url
        if imagen and getattr(imagen.imagen, 'name', None):
            try:
                if default_storage.exists(imagen.imagen.name):
                    return imagen.imagen.url
            except Exception:
                pass
        return settings.MEDIA_URL.rstrip('/') + '/productos_imagenes/default_producto.png'

    def vista_previa(self):
        """Muestra vista previa del producto en admin."""
        # Usar la URL segura que ya hace verificación de existencia
        return format_html(
            '<img src="{}" width="60" height="60" style="object-fit:cover; border-radius:8px; box-shadow:0 0 3px #888;" />',
            self.imagen_principal_url
        )
    vista_previa.short_description = "Vista previa"
    vista_previa.allow_tags = True


# ==============================
# 🖼️ IMAGEN DE PRODUCTO
# ==============================
class ImagenProducto(SoftDeleteModel):
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name='imagenes', verbose_name="Producto"
    )
    imagen = models.ImageField(
        upload_to='productos_imagenes/',
        default='productos_imagenes/default_producto.png',
        verbose_name="Imagen del producto"
    )
    es_principal = models.BooleanField(default=False, verbose_name="¿Es principal?")
    fecha_subida = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de subida")

    class Meta:
        verbose_name = "Imagen de producto"
        verbose_name_plural = "Imágenes de productos"
        ordering = ['-fecha_subida']

    def __str__(self):
        return f"Imagen de {self.producto.nomb_prod}"

    def vista_previa(self):
        """Vista previa de imagen en el admin."""
        if self.imagen and hasattr(self.imagen, 'url'):
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit:cover; border-radius:8px; box-shadow:0 0 3px #888;" />',
                self.imagen.url
            )
        return "(Sin imagen)"
    vista_previa.short_description = "Vista previa"
    vista_previa.allow_tags = True

    def delete(self, using=None, keep_parents=False):
        # Override delete to perform soft delete
        self.soft_delete()
