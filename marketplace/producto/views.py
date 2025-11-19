from django.shortcuts import render, get_object_or_404
from .models import Producto, Categoria, Marca
from django.db.models import Q, Avg, Count
from django.shortcuts import get_object_or_404


def lista_productos(request):
	"""Lista productos. Si se recibe ?categoria=<id> filtra por esa categoría."""
	qs = Producto.objects.filter(estado='disponible').order_by('-fecha_creacion')

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
	producto = get_object_or_404(Producto.objects.select_related('marca', 'tienda').prefetch_related('imagenes', 'categoria', 'resenas__usuario'), pk=pk)

	# obtener imagen principal y las demás
	imagen_principal = producto.imagenes.filter(es_principal=True).first()
	otras_imagenes = producto.imagenes.exclude(pk=imagen_principal.pk) if imagen_principal else producto.imagenes.all()

	categorias = producto.categoria.all()

	# reseñas activas del producto
	reseñas_qs = producto.resenas.filter(is_active=True)
	# agregados: promedio y conteo
	agg = reseñas_qs.aggregate(promedio=Avg('puntuacion'), total=Count('id'))
	promedio_rating = agg.get('promedio') or 0
	reseñas_count = agg.get('total') or 0

	return render(request, 'producto/detalle_producto.html', {
		'producto': producto,
		'imagen_principal': imagen_principal,
		'otras_imagenes': otras_imagenes,
		'categorias': categorias,
		'reseñas': reseñas_qs,
		'promedio_rating': promedio_rating,
		'reseñas_count': reseñas_count,
	})


# --------------------
# API (DRF) ViewSets
# --------------------
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import ProductoSerializer
from marketplace.permissions import IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly
from marketplace.throttles import UserBurstRateThrottle, AnonBurstRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import ProductoFilter
from marketplace.pagination import StandardPageNumberPagination
from django.db import transaction


class ProductoViewSet(viewsets.ModelViewSet):
	"""API ViewSet para Producto con acciones custom."""
	queryset = Producto.objects.all().select_related('marca', 'tienda').prefetch_related('imagenes', 'categoria')
	serializer_class = ProductoSerializer
	permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
	throttle_classes = (UserBurstRateThrottle, AnonBurstRateThrottle)
	filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
	filterset_class = ProductoFilter
	search_fields = ('nomb_prod', 'descripcion')
	ordering_fields = ('precio', 'fecha_creacion', 'stock')
	pagination_class = StandardPageNumberPagination

	@action(detail=True, methods=['post'])
	def set_principal_image(self, request, pk=None):
		"""Marca una imagen del producto como principal.
		Body esperado: {"imagen_id": <id>}"""
		producto = self.get_object()
		imagen_id = request.data.get('imagen_id')
		if not imagen_id:
			return Response({'detail': 'imagen_id requerido.'}, status=status.HTTP_400_BAD_REQUEST)
		imagen = producto.imagenes.filter(pk=imagen_id).first()
		if not imagen:
			return Response({'detail': 'Imagen no encontrada para este producto.'}, status=status.HTTP_404_NOT_FOUND)
		# desmarcar anteriores
		try:
			with transaction.atomic():
				producto.imagenes.update(es_principal=False)
				imagen.es_principal = True
				imagen.save(update_fields=['es_principal'])
		except Exception as e:
			return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
		return Response({'detail': 'Imagen marcada como principal.'})

	@action(detail=True, methods=['get'])
	def promociones(self, request, pk=None):
		"""Devuelve promociones aplicables al producto."""
		producto = self.get_object()
		promos = producto.promociones.filter(fecha_inicio__lte=__import__('django.utils.timezone').utils.timezone.now(), fecha_fin__gte=__import__('django.utils.timezone').utils.timezone.now())
		# enviar IDs y porcentaje
		data = [{'id': p.id, 'descuento_porcentaje': p.descuento_porcentaje} for p in promos]
		return Response(data)
