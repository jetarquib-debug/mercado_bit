from django.core.management.base import BaseCommand
from usuario.scripts.cargar_usuario import ejecutar_carga_usuarios
from django.test import Client, override_settings
from usuario.models import Usuario
from django.contrib.auth.hashers import check_password


class Command(BaseCommand):
    help = 'Carga usuarios de ejemplo y prueba el endpoint de login'

    def handle(self, *args, **options):
        self.stdout.write('Cargando usuarios de prueba...')
        ejecutar_carga_usuarios()

        c = Client()
        self.stdout.write('Probando login con juan.perez@example.com / 123456')

        try:
            u = Usuario.objects.get(email='juan.perez@example.com')
            self.stdout.write(f"DB contrasena (hash): {u.contrasena}")
            self.stdout.write(f"check_password(...) => {check_password('123456', u.contrasena)}")
        except Usuario.DoesNotExist:
            self.stdout.write('Usuario no encontrado en DB')

        with override_settings(ALLOWED_HOSTS=['testserver', 'localhost', '127.0.0.1']):
            resp = c.post('/inicio_sesion/login/', {'email': 'juan.perez@example.com', 'contrasena': '123456'}, follow=True)
        self.stdout.write(f'STATUS: {resp.status_code}')
        self.stdout.write(f'REDIRECT_CHAIN: {resp.redirect_chain}')
        path = resp.request.get('PATH_INFO') if hasattr(resp, 'request') else 'N/A'
        self.stdout.write(f'PATH: {path}')
        # comprobar sesión
        session = c.session
        usuario_id = session.get('usuario_id')
        self.stdout.write(f'SESSION usuario_id: {usuario_id}')
