from django.urls import path
from . import views
from reseña import views as resena_views

app_name = 'producto'

urlpatterns = [
    path('', views.lista_productos, name='lista'),
    path('<int:pk>/', views.detalle_producto, name='detalle'),
    path('<int:pk>/reseñas/crear/', resena_views.crear_reseña, name='crear_reseña'),
]
