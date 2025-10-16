from django.shortcuts import render, redirect
import logging
from django.contrib import messages
from django.db import transaction
from django.urls import reverse_lazy

from .forms import UsuarioRegistrationForm, TiendaRegistrationForm
from usuario.models import CodigoPais
from usuario.models import Pais, Departamento, Provincia, Distrito

def registro_exito(request):
    """Página simple de éxito para mostrar después de un registro."""
    return render(request, 'registrar_usuario_tienda/registro_exito.html')

# --- FUNCIÓN AUXILIAR ---
def procesar_formulario(request, template, context, redirect_url='login'):
    """Función reutilizable para manejar formularios con validación y mensajes."""
    if request.method == "POST":
        for form in context.values():
            if hasattr(form, 'is_valid') and not form.is_valid():
                messages.error(request, "Corrige los errores en el formulario.")
                return render(request, template, context)
        # Si todos los formularios son válidos, devolvemos True
        return True
    return render(request, template, context)


# --- REGISTRO SOLO DE USUARIO ---
def registrar_usuario(request):
    form = UsuarioRegistrationForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        try:
            usuario = form.save()
            messages.success(request, f"Usuario '{usuario.email}' registrado correctamente.")
            return redirect(reverse_lazy('registrar_usuario_tienda:registro_exito'))
        except Exception as e:
            messages.error(request, f"Ocurrió un error al registrar el usuario: {e}")
    elif request.method == "POST":
        messages.error(request, "Corrige los errores del formulario.")
        logging.getLogger(__name__).warning('UsuarioRegistrationForm inválido: %s', form.errors)

    return render(request, "registrar_usuario_tienda/registro_usuario.html", {
        "form": form,
        "codigos": CodigoPais.objects.all(),
        "paises": Pais.objects.all(),
        "departamentos": Departamento.objects.all(),
        "provincias": Provincia.objects.all(),
        "distritos": Distrito.objects.all(),
    })


# --- REGISTRO DE TIENDA (USA FORMULARIO DE USUARIO + TIENDA) ---
@transaction.atomic
def registrar_tienda(request):
    usuario_form = UsuarioRegistrationForm(request.POST or None, request.FILES or None, prefix="usuario")
    tienda_form = TiendaRegistrationForm(request.POST or None, request.FILES or None, prefix="tienda")

    if request.method == "POST" and usuario_form.is_valid() and tienda_form.is_valid():
        try:
            # Guardamos ambos formularios en una sola transacción
            usuario = usuario_form.save()
            tienda = tienda_form.save(usuario=usuario)

            messages.success(
                request,
                f"Tienda '{tienda.nombre_tienda}' creada y usuario '{usuario.email}' registrado correctamente."
            )
            return redirect(reverse_lazy('registrar_usuario_tienda:registro_exito'))

        except Exception as e:
            # Si ocurre un error, la transacción se revierte automáticamente
            messages.error(request, f"Ocurrió un error durante el registro: {e}")

    elif request.method == "POST":
        messages.error(request, "Corrige los errores en los formularios.")
        logging.getLogger(__name__).warning('usuario_form errors: %s', usuario_form.errors)
        logging.getLogger(__name__).warning('tienda_form errors: %s', tienda_form.errors)

    return render(request, "registrar_usuario_tienda/registro_tienda.html", {
        "usuario_form": usuario_form,
        "tienda_form": tienda_form,
        "codigos": CodigoPais.objects.all(),
        "paises": Pais.objects.all(),
        "departamentos": Departamento.objects.all(),
        "provincias": Provincia.objects.all(),
        "distritos": Distrito.objects.all(),
    })



