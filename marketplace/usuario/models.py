from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils.html import format_html
from django.core.files.storage import default_storage
from django.conf import settings
from marketplace.utils.softdelete import SoftDeleteModel


# ==============================
# 📸 IMAGEN PERFIL USUARIO
# ==============================
class ImagenPerfilUsuario(SoftDeleteModel):
    imagen = models.ImageField(
        upload_to='usuario/',
        default='usuario/default.png'
    )
    fecha_subida = models.DateTimeField(auto_now_add=True)
    es_principal = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Imagen de Perfil"
        verbose_name_plural = "Imágenes de Perfiles"
        ordering = ['-fecha_subida']

    def __str__(self):
        return f"Imagen {self.id} ({'Principal' if self.es_principal else 'Secundaria'})"

    # 🖼️ Mostrar imagen en admin
    def vista_previa(self):
        # Verificación: si la imagen no existe en storage, usar placeholder
        if self.imagen and getattr(self.imagen, 'name', None):
            try:
                if default_storage.exists(self.imagen.name):
                    return format_html('<img src="{}" width="70" height="70" style="border-radius:8px; object-fit:cover;" />', self.imagen.url)
            except Exception:
                pass
        default_url = settings.MEDIA_URL.rstrip('/') + '/usuario/default.png'
        return format_html('<img src="{}" width="70" height="70" style="border-radius:8px; object-fit:cover;" />', default_url)
    vista_previa.short_description = "Vista previa"


# ==============================
# 🌍 UBICACIÓN GEOGRÁFICA
# ==============================
class Pais(SoftDeleteModel):
    nomb_pais = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "País"
        verbose_name_plural = "Países"
        ordering = ['nomb_pais']

    def __str__(self):
        return self.nomb_pais


class Departamento(SoftDeleteModel):
    nomb_departamento = models.CharField(max_length=100)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name='departamentos')

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
        ordering = ['nomb_departamento']

    def __str__(self):
        return self.nomb_departamento


class Provincia(SoftDeleteModel):
    nomb_provincia = models.CharField(max_length=100)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='provincias')

    class Meta:
        verbose_name = "Provincia"
        verbose_name_plural = "Provincias"
        ordering = ['nomb_provincia']

    def __str__(self):
        return self.nomb_provincia


class Distrito(SoftDeleteModel):
    nomb_distrito = models.CharField(max_length=100)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE, related_name='distritos')

    class Meta:
        verbose_name = "Distrito"
        verbose_name_plural = "Distritos"
        ordering = ['nomb_distrito']

    def __str__(self):
        return self.nomb_distrito


# ==============================
# ☎️ CÓDIGO DE PAÍS
# ==============================
class CodigoPais(SoftDeleteModel):
    pais = models.OneToOneField(
        Pais,
        on_delete=models.CASCADE,
        related_name='codigo_pais'
    )
    codigo = models.CharField(max_length=10, unique=True)
    imagen_pais = models.ImageField(
        upload_to='codigo_pais/',
        null=True,
        blank=True,
        default='codigo_pais/default_bandera.png'
    )

    class Meta:
        verbose_name = "Código de País"
        verbose_name_plural = "Códigos de País"
        ordering = ['pais__nomb_pais']

    def __str__(self):
        return f"(+{self.codigo}) {self.pais.nomb_pais}"

    # 🏳️ Mostrar bandera en el admin
    def bandera(self):
        # Verificar existencia del archivo de bandera en storage
        if self.imagen_pais and getattr(self.imagen_pais, 'name', None):
            try:
                if default_storage.exists(self.imagen_pais.name):
                    return format_html('<img src="{}" width="40" height="25" style="object-fit:cover; border:1px solid #ddd;" />', self.imagen_pais.url)
            except Exception:
                pass
        default_url = settings.MEDIA_URL.rstrip('/') + '/codigo_pais/default_bandera.png'
        return format_html('<img src="{}" width="40" height="25" style="object-fit:cover; border:1px solid #ddd;" />', default_url)
    bandera.short_description = "Bandera"


# ==============================
# 👤 USUARIO
# ==============================
class Usuario(SoftDeleteModel):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    nombres = models.CharField(max_length=100, null=True, blank=True)
    apellidos = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=255)

    imagenes = models.ManyToManyField(
        ImagenPerfilUsuario,
        blank=True,
        related_name='usuarios'
    )

    codigo_pais = models.ForeignKey(
        CodigoPais,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='usuarios'
    )
    telefono = models.CharField(max_length=20, null=True, blank=True)
    direccion = models.CharField(max_length=200, null=True, blank=True)
    pais = models.ForeignKey(
        Pais,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='usuarios'
    )
    departamento = models.ForeignKey(
        Departamento,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='usuarios'
    )
    provincia = models.ForeignKey(
        Provincia,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='usuarios'
    )

    distrito = models.ForeignKey(
        Distrito,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='usuarios'
    )

    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    dni_ce = models.BigIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"{self.nombres or ''} {self.apellidos or ''} - {self.email}"

    # 🔒 Guardar contraseña encriptada automáticamente
    def save(self, *args, **kwargs):
        if not self.pk or 'pbkdf2_' not in self.contrasena:  # evita re-hash si ya está encriptada
            self.contrasena = make_password(self.contrasena)
        super().save(*args, **kwargs)

    # 🧩 Propiedad: imagen principal
    @property
    def imagen_principal(self):
        # Retornar URL segura: comprobar que el archivo existe
        img = self.imagenes.filter(es_principal=True).first()
        if img and getattr(img.imagen, 'name', None):
            try:
                if default_storage.exists(img.imagen.name):
                    return img.imagen.url
            except Exception:
                pass
        return settings.MEDIA_URL.rstrip('/') + '/usuario/default.png'

    # 🖼️ Mostrar en admin
    def vista_previa(self):
        return format_html(
            '<img src="{}" width="60" height="60" style="border-radius:50%; object-fit:cover;" />',
            self.imagen_principal
        )
    vista_previa.short_description = "Foto Perfil"

    def delete(self, using=None, keep_parents=False):
        # Soft delete user and related images
        for img in self.imagenes.all():
            try:
                img.soft_delete()
            except Exception:
                pass
        self.soft_delete()
