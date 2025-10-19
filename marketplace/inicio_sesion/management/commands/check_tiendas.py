from django.core.management.base import BaseCommand


class Command(BaseCommand):
	help = 'Crea usuarios y tiendas de prueba y simula logins para comprobar la lógica de bloqueo.'

	def handle(self, *args, **options):
		from inicio_sesion.scripts.test_login_tiendas import ejecutar_test
		ejecutar_test()

