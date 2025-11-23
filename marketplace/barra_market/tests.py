from django.test import TestCase
from django.urls import reverse
import json

from producto.models import Categoria, Marca


class ApiCategoriasMarcasTests(TestCase):
	def test_api_returns_empty_lists_when_no_data(self):
		"""Si no hay categorias ni marcas, el endpoint devuelve listas vacías."""
		resp = self.client.get('/api/categorias/')
		self.assertEqual(resp.status_code, 200)
		data = resp.json()
		self.assertIn('categorias', data)
		self.assertIn('marcas', data)
		self.assertEqual(data['categorias'], [])
		self.assertEqual(data['marcas'], [])

	def test_api_returns_categorias_and_marcas(self):
		"""Comprueba que el endpoint devuelve los objetos creados con campos esperados."""
		c1 = Categoria.objects.create(nomb_ca='Celulares')
		c2 = Categoria.objects.create(nomb_ca='Audio')
		m1 = Marca.objects.create(nomb_marca='MarcaX')

		resp = self.client.get('/api/categorias/')
		self.assertEqual(resp.status_code, 200)
		data = resp.json()
		self.assertIsInstance(data.get('categorias'), list)
		self.assertIsInstance(data.get('marcas'), list)

		# comprobar que aparecen las entradas y que tienen keys id/nombre
		categorias_nombres = {c['nomb_ca'] for c in data['categorias']}
		marcas_nombres = {m['nomb_marca'] for m in data['marcas']}
		self.assertIn('Celulares', categorias_nombres)
		self.assertIn('Audio', categorias_nombres)
		self.assertIn('MarcaX', marcas_nombres)
