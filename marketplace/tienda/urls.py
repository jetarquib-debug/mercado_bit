
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .viewsets import TiendaViewSet

app_name = 'tienda'

router = DefaultRouter()
router.register(r'api/v1/tiendas', TiendaViewSet, basename='tienda')

urlpatterns = [
    # Perfil general (usuario autenticado que no indica tienda concreta)
    path('perfil/', views.perfil_tienda, name='perfil'),
    # Perfil de tienda por id (ej: /tienda/perfil/5/)
    path('perfil/<int:pk>/', views.perfil_tienda, name='perfil_pk'),
    # Perfil comercial con panel y acciones (ej: /tienda/perfil/comercial/5/)
    path('perfil/comercial/<int:pk>/', views.perfil_tienda_comercial, name='perfil_comercial'),
    path('', include(router.urls)),
]
