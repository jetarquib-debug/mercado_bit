from rest_framework.routers import DefaultRouter
from django.urls import path, include

from producto.views import ProductoViewSet
from tienda.views import TiendaViewSet
from usuario.views import UsuarioViewSet
from carrito.views import CarritoViewSet
from detalles_pedidos.views import DetalleOrdenViewSet
from detalle_orden.views import OrdenViewSet
from promociones.views import PromocionViewSet
from pago.views import PagoViewSet, MetodoPagoViewSet

router = DefaultRouter()
router.register(r'productos', ProductoViewSet, basename='producto')
router.register(r'tiendas', TiendaViewSet, basename='tienda')
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'carritos', CarritoViewSet, basename='carrito')
router.register(r'detalles', DetalleOrdenViewSet, basename='detalleorden')
router.register(r'ordenes', OrdenViewSet, basename='orden')
router.register(r'promociones', PromocionViewSet, basename='promocion')
router.register(r'pagos', PagoViewSet, basename='pago')
router.register(r'metodos_pago', MetodoPagoViewSet, basename='metodopago')

urlpatterns = [
    path('', include(router.urls)),
]
