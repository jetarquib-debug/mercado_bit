from django.core.management.base import BaseCommand
from django.test import Client, override_settings
from usuario.models import Usuario, Pais, Departamento, Provincia, Distrito, CodigoPais
from tienda.models import Tienda


class Command(BaseCommand):
    help = 'Crea 3 usuarios, les asigna una tienda y prueba el endpoint de login para verificar bloqueo.'

    def handle(self, *args, **options):
        self.stdout.write('=== Creando/actualizando ubicaciones base necesarias ===')

        pais, _ = Pais.objects.get_or_create(nomb_pais='Perú')
        departamento, _ = Departamento.objects.get_or_create(nomb_departamento='Lima', pais=pais)
        provincia, _ = Provincia.objects.get_or_create(nomb_provincia='Lima', departamento=departamento)
        distrito, _ = Distrito.objects.get_or_create(nomb_distrito='Miraflores', provincia=provincia)
        codigo_pais, _ = CodigoPais.objects.get_or_create(pais=pais, defaults={'codigo': '51'})

        usuarios_data = [
            ('test1@example.com', 'Test1', 'One', 'pass1'),
            ('test2@example.com', 'Test2', 'Two', 'pass2'),
            ('test3@example.com', 'Test3', 'Three', 'pass3'),
        ]

        usuarios = []
        for email, nombres, apellidos, pwd in usuarios_data:
            u, created = Usuario.objects.get_or_create(email=email, defaults={
                'nombres': nombres,
                'apellidos': apellidos,
                'contrasena': pwd,
                'pais': pais,
                'codigo_pais': codigo_pais,
                'departamento': departamento,
                'provincia': provincia,
                'distrito': distrito,
            })
            if not created:
                # actualizar datos y contraseña (save() del modelo encripta)
                u.nombres = nombres
                u.apellidos = apellidos
                u.contrasena = pwd
                u.pais = pais
                u.codigo_pais = codigo_pais
                u.departamento = departamento
                u.provincia = provincia
                u.distrito = distrito
                u.save()
                self.stdout.write(f'⚠️ Usuario actualizado: {email}')
            else:
                self.stdout.write(f'✅ Usuario creado: {email}')
            usuarios.append((u, pwd))

        # Crear una tienda para CADA usuario (deberían quedar bloqueados)
        for u, pwd in usuarios:
            tienda_email = f"tienda_{u.email}"
            tienda, creada = Tienda.objects.get_or_create(usuario=u, defaults={
                'nombre_tienda': f"Tienda de {u.nombres}",
                'descripcion': 'Tienda creada por script de prueba',
                'email': tienda_email,
                'codigo_pais': codigo_pais,
                'telefono': u.telefono or '000',
                'direccion': u.direccion or 'Direccion prueba',
                'pais': pais,
                'departamento': departamento,
                'provincia': provincia,
                'distrito': distrito,
                'ruc': '99999999999',
            })
            if creada:
                self.stdout.write(f'✅ Tienda creada para {u.email}: {tienda.nombre_tienda}')
            else:
                self.stdout.write(f'⚠️ Tienda ya existía para {u.email}: {tienda.nombre_tienda}')

        # Ahora probar login vía endpoint
        c = Client()
        with override_settings(ALLOWED_HOSTS=['testserver', 'localhost', '127.0.0.1']):
            for u, pwd in usuarios:
                self.stdout.write(f'--- Probando login para {u.email} ---')
                resp = c.post('/inicio_sesion/login/', {'email': u.email, 'contrasena': pwd}, follow=True)
                status = resp.status_code
                # comprobar si sesión tiene usuario_id
                ses_id = c.session.get('usuario_id')
                self.stdout.write(f'STATUS: {status} | SESSION usuario_id: {ses_id} | REDIRECT_CHAIN: {resp.redirect_chain}')
                # limpiar sesión entre intentos
                c.session.flush()

        self.stdout.write('=== Test finalizado ===')
