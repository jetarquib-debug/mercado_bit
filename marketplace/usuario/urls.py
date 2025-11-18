
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .viewsets import UsuarioViewSet

app_name = 'usuario'

router = DefaultRouter()
router.register(r'api/usuarios', UsuarioViewSet, basename='usuario')

urlpatterns = [
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('', include(router.urls)),
]
