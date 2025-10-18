from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages

from .forms import LoginForm


def login_view(request):
	"""Procesa el formulario de inicio de sesión. Si es POST autentica y hace login,
	si es GET devuelve el formulario vacío. Esta vista está pensada también
	para ser incluida como fragmento en `home.html` (render via include).
	"""
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			messages.success(request, f'Bienvenido {user.get_username()}')
			# Redirigir a la página desde donde vino o al home
			next_url = request.POST.get('next') or request.GET.get('next')
			if next_url:
				return redirect(next_url)
			return redirect('home')
	else:
		form = LoginForm()
	# Si la plantilla se incluye dentro de home, request puede requerir el context
	return render(request, 'inicio_sesion/iniciar_sesion.html', {'form': form})
