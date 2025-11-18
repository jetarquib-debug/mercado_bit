from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import viewsets as vs
from .views_external import WeatherAPIView, ExchangeAPIView

router = DefaultRouter()
router.register(r'productos', vs.ProductoViewSet, basename='producto')
router.register(r'usuarios', vs.UsuarioViewSet, basename='usuario')
router.register(r'tiendas', vs.TiendaViewSet, basename='tienda')
router.register(r'carritos', vs.CarritoViewSet, basename='carrito')
router.register(r'detalles', vs.DetalleOrdenViewSet, basename='detalleorden')
router.register(r'ordenes', vs.OrdenViewSet, basename='orden')
router.register(r'metodos_pago', vs.MetodoPagoViewSet, basename='metodopago')
router.register(r'pagos', vs.PagoViewSet, basename='pago')
router.register(r'promociones', vs.PromocionViewSet, basename='promocion')

urlpatterns = [
    path('weather/', WeatherAPIView.as_view(), name='weather-api'),
    path('exchange/', ExchangeAPIView.as_view(), name='exchange-api'),
    path('', include(router.urls)),
]
