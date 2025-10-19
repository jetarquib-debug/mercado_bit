from .models import Usuario


def usuario_actual(request):
    """Context processor que añade 'usuario_profile' al contexto de las plantillas
    si el usuario ha iniciado sesión mediante el sistema personalizado (session).
    """
    usuario = None
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        try:
            usuario = Usuario.objects.filter(id=usuario_id).first()
        except Exception:
            usuario = None

    return {'usuario_profile': usuario}
