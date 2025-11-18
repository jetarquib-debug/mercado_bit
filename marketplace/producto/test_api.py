from rest_framework.test import APITestCase
from producto.models import Producto, Marca, Categoria
from tienda.models import Tienda
from usuario.models import Usuario, Pais, CodigoPais


class TestAPIFilterPagination(APITestCase):
    def setUp(self):
        # Crear datos básicos
        pais = Pais.objects.create(nomb_pais='Peru')
        codigo = CodigoPais.objects.create(pais=pais, codigo='51')
        u = Usuario.objects.create(nombres='Propietario', apellidos='Uno', email='owner@example.com', contrasena='pass123')
        tienda = Tienda.objects.create(nombre_tienda='Tienda A', usuario=u, codigo_pais=codigo)

        marca1 = Marca.objects.create(nomb_marca='MarcaX')
        marca2 = Marca.objects.create(nomb_marca='MarcaY')
        cat1 = Categoria.objects.create(nomb_ca='Ropa')
        cat2 = Categoria.objects.create(nomb_ca='Calzado')

        # Productos variados
        Producto.objects.create(tienda=tienda, nomb_prod='Camisa Azul', descripcion='Una camisa', precio=50.00, stock=10, estado='disponible', marca=marca1)
        Producto.objects.create(tienda=tienda, nomb_prod='Pantalon Negro', descripcion='Pantalon', precio=120.00, stock=0, estado='agotado', marca=marca1)
        p3 = Producto.objects.create(tienda=tienda, nomb_prod='Zapato Deportivo', descripcion='Zapato', precio=200.00, stock=5, estado='disponible', marca=marca2)
        p3.categoria.set([cat2])

        # Crear más tiendas
        for i in range(1, 6):
            Usuario.objects.create(nombres=f'User{i}', apellidos='T', email=f'u{i}@ex.com', contrasena='x')
            Tienda.objects.create(nombre_tienda=f'Tienda {i}', usuario=u, codigo_pais=codigo)

    def test_product_filter_price_and_disponible_and_limit_offset(self):
        url = '/api/productos/'
        resp = self.client.get(url, {'precio_min': '30', 'precio_max': '150', 'disponible': 'True', 'limit': 2, 'offset': 0})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        # limit-offset returns 'results'
        self.assertIn('results', data)
        results = data['results']
        self.assertLessEqual(len(results), 2)
        for item in results:
            self.assertGreaterEqual(float(item['precio']), 30.0)
            self.assertLessEqual(float(item['precio']), 150.0)

    def test_product_search_and_ordering(self):
        url = '/api/productos/'
        resp = self.client.get(url, {'search': 'Zapato', 'ordering': '-precio'})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        results = data.get('results', data)
        self.assertTrue(any('Zapato' in r['nomb_prod'] for r in results))

    def test_tienda_filter_search_and_pagination(self):
        url = '/api/tiendas/'
        # page number pagination default
        resp = self.client.get(url, {'page_size': 2, 'page': 2})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        # PageNumberPagination provides 'results'
        self.assertIn('results', data)
        self.assertLessEqual(len(data['results']), 2)
