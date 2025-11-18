
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .viewsets import ProductoViewSet

app_name = 'producto'

router = DefaultRouter()
router.register(r'api/productos', ProductoViewSet, basename='producto')

urlpatterns = [
    path('', views.lista_productos, name='lista'),
    path('<int:pk>/', views.detalle_producto, name='detalle'),
    path('', include(router.urls)),
]
