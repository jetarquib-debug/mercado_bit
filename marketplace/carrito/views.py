from django.shortcuts import render


def ver_carrito(request):
	"""Render view for carrito page. Cart is managed client-side via localStorage."""
	return render(request, 'carrito/carrito.html')

# Create your views here.
