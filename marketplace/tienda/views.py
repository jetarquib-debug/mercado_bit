from django.shortcuts import render, get_object_or_404
from .models import Tienda


def perfil_tienda(request, pk=None):
	"""Renderiza la página de perfil de la tienda.
	Si se pasa `pk`, carga la Tienda correspondiente; si no, renderiza una vista genérica.
	"""
	tienda = None
	if pk is not None:
		tienda = get_object_or_404(Tienda, pk=pk)

	return render(request, 'perfil_tienda.html', {'tienda': tienda})
