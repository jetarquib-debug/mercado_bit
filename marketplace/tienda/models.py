from django.db import models
from usuario.models import Usuario, CodigoPais, Distrito, Provincia, Departamento, Pais
from django.utils.html import format_html

# --- IMAGEN DE PERFIL DE TIENDA ---
class ImagenPerfilTienda(models.Model):
    imagen = models.ImageField(
        upload_to='tienda/',
        default='tienda/default.png',
        verbose_name="Imagen"
    )
    fecha_subida = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de subida")
    es_principal = models.BooleanField(default=False, verbose_name="¿Es principal?")

    class Meta:
        verbose_name = "Imagen de tienda"
        verbose_name_plural = "Imágenes de tiendas"
        ordering = ['-es_principal', '-fecha_subida']

    def __str__(self):
        return f"Imagen ({'Principal' if self.es_principal else 'Secundaria'}) - {self.fecha_subida:%Y-%m-%d}"

    # 🖼️ Vista previa para el admin
    def vista_previa(self):
        if self.imagen:
            return format_html(
                '<img src="{}" width="80" height="80" style="border-radius:8px; object-fit:cover;" />',
                self.imagen.url
            )
        return "(Sin imagen)"

    vista_previa.short_description = "Vista previa"

# --- MODELO TIENDA ---
class Tienda(models.Model):
    nombre_tienda = models.CharField(max_length=150, verbose_name="Nombre de la tienda")
    descripcion = models.CharField(max_length=255, null=True, blank=True, verbose_name="Descripción")
    email = models.EmailField(unique=True, null=True, blank=True, verbose_name="Correo electrónico")

    codigo_pais = models.ForeignKey(
        CodigoPais, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='tiendas', verbose_name="Código del país"
    )
    telefono = models.CharField(max_length=20, null=True, blank=True, verbose_name="Teléfono")
    direccion = models.CharField(max_length=200, null=True, blank=True, verbose_name="Dirección")

    distrito = models.ForeignKey(
        Distrito, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='tiendas', verbose_name="Distrito"
    )
    provincia = models.ForeignKey(
        Provincia, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='tiendas', verbose_name="Provincia"
    )
    departamento = models.ForeignKey(
        Departamento, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='tiendas', verbose_name="Departamento"
    )
    pais = models.ForeignKey(
        Pais, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='tiendas', verbose_name="País"
    )

    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    ruc = models.CharField(max_length=11, null=True, blank=True, verbose_name="RUC")

    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name='tienda', verbose_name="Usuario propietario"
    )

    imagenes = models.ManyToManyField(
        ImagenPerfilTienda, blank=True, related_name='tiendas', verbose_name="Imágenes"
    )

    class Meta:
        verbose_name = "Tienda"
        verbose_name_plural = "Tiendas"
        ordering = ['nombre_tienda']
        constraints = [
            models.UniqueConstraint(fields=['usuario'], name='unique_usuario_tienda')
        ]

    def __str__(self):
        # Evitar usar `username` porque el modelo `Usuario` personalizado puede no tenerlo.
        # Mostrar preferentemente el email, si no está disponible usar nombres/apellidos.
        usuario_repr = None
        try:
            usuario_repr = getattr(self.usuario, 'email', None)
        except Exception:
            usuario_repr = None
        if not usuario_repr:
            nombres = getattr(self.usuario, 'nombres', '') or ''
            apellidos = getattr(self.usuario, 'apellidos', '') or ''
            usuario_repr = f"{(nombres + ' ' + apellidos).strip()}" or "Usuario"
        return f"{self.nombre_tienda} ({usuario_repr})"

    # --- PROPERTIES ÚTILES ---
    @property
    def imagen_principal(self):
        """Devuelve la imagen principal o una por defecto."""
        principal = self.imagenes.filter(es_principal=True).first()
        if principal:
            return principal.imagen.url
        return '/media/tienda/default.png'

    @property
    def ubicacion_completa(self):
        """Muestra la ubicación concatenando todos los niveles disponibles."""
        partes = [self.distrito, self.provincia, self.departamento, self.pais]
        return ", ".join([str(p) for p in partes if p])

    @property
    def telefono_formateado(self):
        """Devuelve el teléfono con prefijo del país si existe."""
        if self.codigo_pais:
            return f"+{self.codigo_pais.pais.codigo} {self.telefono or ''}".strip()
        return self.telefono or "Sin teléfono"

    def imagenes_contador(self):
        """Cantidad de imágenes asociadas."""
        return self.imagenes.count()
