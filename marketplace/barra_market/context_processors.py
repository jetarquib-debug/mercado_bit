from producto.models import Categoria, Marca


def global_nav(request):
    """Context processor que añade `categorias` y `marcas` al contexto global
    para que el menú y el panel puedan renderizarse en cualquier plantilla.
    """
    try:
        categorias = Categoria.objects.all().order_by('nomb_ca')
    except Exception:
        categorias = []
    try:
        marcas = Marca.objects.all().order_by('nomb_marca')
    except Exception:
        marcas = []

    return {
        'categorias': categorias,
        'marcas': marcas,
    }
