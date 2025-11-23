from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Página principal
    # Endpoint usado por el frontend como fallback para obtener categorías y marcas
    path('api/categorias/', views.api_categorias_marcas, name='api_categorias_marcas'),
]
