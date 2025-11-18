from django.urls import path
from . import views

app_name = 'carrito'

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import CarritoViewSet

urlpatterns = [
    path('', views.ver_carrito, name='ver'),
]

router = DefaultRouter()
router.register(r'api/v1/carritos', CarritoViewSet, basename='carrito')

urlpatterns += [
    path('', include(router.urls)),
]
