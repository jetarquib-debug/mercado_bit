from django.shortcuts import render, get_object_or_404
from .models import Tienda
from producto.models import Producto
from django.db.models import Sum, Count


def perfil_tienda(request, pk=None):
	"""Renderiza la página de perfil de la tienda.
	Si se pasa `pk`, carga la Tienda correspondiente; si no, renderiza una vista genérica.
	"""
	tienda = None
	if pk is not None:
		tienda = get_object_or_404(Tienda, pk=pk)

	return render(request, 'perfil_tienda.html', {'tienda': tienda})


def perfil_tienda_comercial(request, pk):
	"""Vista comercial de la tienda: muestra panel con botones para info, productos, stock y acciones comerciales."""
	tienda = get_object_or_404(Tienda, pk=pk)

	# productos de la tienda
	productos_qs = Producto.objects.filter(tienda=tienda).select_related('marca')
	productos = list(productos_qs)

	# estadísticas simples
	total_productos = productos_qs.count()
	en_stock = productos_qs.filter(stock__gt=0).count()
	agotados = productos_qs.filter(stock__lte=0).count()

	return render(request, 'perfil_tienda_comercial.html', {
		'tienda': tienda,
		'productos': productos,
		'total_productos': total_productos,
		'en_stock': en_stock,
		'agotados': agotados,
	})
