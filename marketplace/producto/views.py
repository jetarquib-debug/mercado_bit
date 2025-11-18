from django.shortcuts import render, get_object_or_404
from .models import Producto, Categoria, Marca
from django.db.models import Q
from django.shortcuts import get_object_or_404


def lista_productos(request):
	"""Lista productos. Si se recibe ?categoria=<id> filtra por esa categoría."""
	qs = Producto.objects.filter(estado='disponible', is_active=True).order_by('-fecha_creacion')

	# búsqueda por texto (q)
	q_text = request.GET.get('q', '').strip()
	if q_text:
		# buscar por nombre o descripción
		qs = qs.filter(
			Q(nomb_prod__icontains=q_text) | Q(descripcion__icontains=q_text)
		)

	# Soportar múltiples categorías y marcas mediante parámetros GET repetidos
	selected_categoria_ids = request.GET.getlist('categoria')  # lista de strings
	selected_marca_ids = request.GET.getlist('marca')

	categoria_seleccionada = None
	marca_seleccionada = None

	# Filtrar por categorías (si se proporcionan)
	if selected_categoria_ids:
		# convertir a ints donde sea posible
		try:
			cat_ids = [int(x) for x in selected_categoria_ids if x.isdigit()]
			if cat_ids:
				qs = qs.filter(categoria__pk__in=cat_ids)
				# tomar la primera como 'seleccionada' para mostrar nombre
				categoria_seleccionada = Categoria.objects.filter(pk=cat_ids[0]).first()
				# también obtener todas las categorías seleccionadas para mostrarlas
				selected_categorias = list(Categoria.objects.filter(pk__in=cat_ids))
		except Exception:
			pass

	# Filtrar por marcas (si se proporcionan)
	if selected_marca_ids:
		try:
			mar_ids = [int(x) for x in selected_marca_ids if x.isdigit()]
			if mar_ids:
				qs = qs.filter(marca__pk__in=mar_ids)
				marca_seleccionada = Marca.objects.filter(pk=mar_ids[0]).first()
				selected_marcas = list(Marca.objects.filter(pk__in=mar_ids))
		except Exception:
			pass

	productos = qs[:50]
	categorias = Categoria.objects.all().order_by('nomb_ca')
	marcas = Marca.objects.all().order_by('nomb_marca')

	# convertir listas seleccionadas a enteros para la plantilla
	try:
		selected_categoria_ints = [int(x) for x in selected_categoria_ids if x.isdigit()]
	except Exception:
		selected_categoria_ints = []
	try:
		selected_marca_ints = [int(x) for x in selected_marca_ids if x.isdigit()]
	except Exception:
		selected_marca_ints = []

	# asegurarse de que las listas de objetos existen
	if 'selected_categorias' not in locals():
		selected_categorias = []
	if 'selected_marcas' not in locals():
		selected_marcas = []

	return render(request, 'producto/lista_productos.html', {
		'productos': productos,
		'categorias': categorias,
		'marcas': marcas,
		'selected_categoria_ids': selected_categoria_ids,
		'selected_marca_ids': selected_marca_ids,
		'selected_categoria_ints': selected_categoria_ints,
		'selected_marca_ints': selected_marca_ints,
		'categoria_seleccionada': categoria_seleccionada,
		'marca_seleccionada': marca_seleccionada,
		'selected_categorias': selected_categorias,
		'selected_marcas': selected_marcas,
		'query': q_text,
	})


def detalle_producto(request, pk):
	"""Muestra la ficha completa de un producto identificado por su pk."""
	producto = get_object_or_404(Producto.objects.select_related('marca', 'tienda').prefetch_related('imagenes', 'categoria'), pk=pk)

	# obtener imagen principal y las demás
	imagen_principal = producto.imagenes.filter(es_principal=True).first()
	otras_imagenes = producto.imagenes.exclude(pk=imagen_principal.pk) if imagen_principal else producto.imagenes.all()

	categorias = producto.categoria.all()

	return render(request, 'producto/detalle_producto.html', {
		'producto': producto,
		'imagen_principal': imagen_principal,
		'otras_imagenes': otras_imagenes,
		'categorias': categorias,
	})
