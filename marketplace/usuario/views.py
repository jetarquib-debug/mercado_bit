from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Usuario


def perfil_usuario(request):
	usuario_id = request.session.get('usuario_id')
	if not usuario_id:
		messages.info(request, 'Debes iniciar sesión para ver tu perfil.')
		return redirect('inicio_sesion:login')

	usuario = get_object_or_404(Usuario, pk=usuario_id)

	context = {
		'usuario': usuario,
	}
	return render(request, 'perfil_usuario.html', context)
