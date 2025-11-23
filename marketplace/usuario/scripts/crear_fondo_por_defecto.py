# script para crear registro de fondo por defecto
# Ejecutar desde manage.py shell: exec(open('usuario/scripts/crear_fondo_por_defecto.py').read())
from django.conf import settings
from usuario.models import FondoPantallaUsuario

# Ruta relativa en MEDIA
default_path = 'usuario/fondo_de_pantalla.jpg'

# Crear si no existe
if not FondoPantallaUsuario.objects.filter(is_default=True).exists():
    f = FondoPantallaUsuario.objects.create(usuario=None, imagen=default_path, is_default=True, is_active=False)
    print('Fondo por defecto creado:', f)
else:
    print('Ya existe un fondo por defecto.')
