import os
import django
import json
from datetime import datetime, timedelta


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace.settings')
django.setup()

from django.test import Client

from usuario.models import Usuario
from tienda.models import Tienda
from producto.models import Producto, Marca, Categoria
from promociones.models import Promocion


def ensure_user():
    user, created = Usuario.objects.get_or_create(email='apitest@example.com', defaults={'contrasena': 'testpass', 'nombres': 'Api', 'apellidos': 'Test'})
    if created:
        print('Usuario creado:', user.email)
    return user


def ensure_tienda(user):
    tienda, created = Tienda.objects.get_or_create(nombre_tienda='TiendaAPI', usuario=user, defaults={'email': 'tienda@example.com'})
    if created:
        print('Tienda creada:', tienda.nombre_tienda)
    return tienda


def create_sample_products(tienda):
    marca, _ = Marca.objects.get_or_create(nomb_marca='MarcaAPI')
    cat1, _ = Categoria.objects.get_or_create(nomb_ca='CatA')
    cat2, _ = Categoria.objects.get_or_create(nomb_ca='CatB')

    # crear varios productos con precios distintos
    Producto.objects.all().delete()
    prods = []
    for i, precio in enumerate([5, 15, 25, 50, 75, 150]):
        p = Producto.objects.create(tienda=tienda, nomb_prod=f'Producto {i}', precio=precio, stock=10+i, peso=1.0, estado='disponible')
        p.marca = marca
        p.save()
        p.categoria.add(cat1 if i % 2 == 0 else cat2)
        prods.append(p)
    print('Productos creados:', len(prods))
    return prods


def create_sample_promotions(products):
    Promocion.objects.all().delete()
    promos = []
    ahora = datetime.utcnow()
    # crear 25 promociones para paginación
    for i in range(25):
        inicio = ahora - timedelta(days=1)
        fin = ahora + timedelta(days=30)
        promo = Promocion.objects.create(descripcion=f'Promo {i}', descuento_porcentaje=5 + i % 20, fecha_inicio=inicio, fecha_fin=fin)
        # asociar a algunos productos
        if i % 3 == 0:
            promo.productos.add(products[i % len(products)])
        promos.append(promo)
    print('Promociones creadas:', len(promos))
    return promos


def run_tests():
    client = Client()

    user = ensure_user()
    tienda = ensure_tienda(user)
    products = create_sample_products(tienda)
    promos = create_sample_promotions(products)

    print('\n== Probando filtro de productos: precio_min=20 & precio_max=100 ==')
    resp = client.get('/api/productos/', {'precio_min': 20, 'precio_max': 100, 'page_size': 50})
    print('status:', resp.status_code)
    try:
        data = resp.json()
    except Exception:
        print('Respuesta no JSON:', resp.content[:200])
        return
    # Para PageNumberPagination, datos están en 'results'
    results = data.get('results', data)
    print('Productos devueltos:', len(results))
    for p in results:
        print('-', p.get('nomb_prod'), 'precio=', p.get('precio'))

    print('\n== Probando paginación de promociones: limit=5 offset=0 ==')
    resp2 = client.get('/api/promociones/', {'limit': 5, 'offset': 0})
    print('status:', resp2.status_code)
    try:
        data2 = resp2.json()
    except Exception:
        print('Respuesta no JSON:', resp2.content[:200])
        return
    results2 = data2.get('results', data2)
    print('Promociones devueltas (limit=5):', len(results2))
    print('Total count (si disponible):', data2.get('count'))


if __name__ == '__main__':
    run_tests()
