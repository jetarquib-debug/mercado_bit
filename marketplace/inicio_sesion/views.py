from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from usuario.models import Usuario
from tienda.models import Tienda
from .forms import LoginUsuarioForm


def login_usuario(request):
	if request.method == "POST":
		form = LoginUsuarioForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data["email"]
			contrasena = form.cleaned_data["contrasena"]

			try:
				usuario = Usuario.objects.get(email=email)
			except Usuario.DoesNotExist:
				messages.error(request, "No existe un usuario con ese correo.")
				return render(request, "inicio_sesion/iniciar_sesion.html", {"form": form})

			if check_password(contrasena, usuario.contrasena):
				# Si el usuario ya posee una tienda, redirigir al perfil de su tienda
				tienda = Tienda.objects.filter(usuario=usuario).first()
				if tienda:
					# Redirigir al perfil de la tienda (ruta con pk)
					return redirect('tienda:perfil_pk', pk=tienda.pk)

				request.session["usuario_id"] = usuario.id
				request.session["usuario_nombre"] = usuario.nombres
				messages.success(request, f"Bienvenido, {usuario.nombres} 👋")
				return redirect('usuario:perfil')
			else:
				messages.error(request, "Contraseña incorrecta.")
	else:
		form = LoginUsuarioForm()

	return render(request, "inicio_sesion/iniciar_sesion.html", {"form": form})


def logout_usuario(request):
	request.session.flush()
	messages.info(request, "Sesión cerrada correctamente 👋")
	return redirect('inicio_sesion:login')
