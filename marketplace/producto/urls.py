from django.urls import path
from . import views

app_name = 'producto'

urlpatterns = [
    path('', views.lista_productos, name='lista'),
    path('<int:pk>/', views.detalle_producto, name='detalle'),
]
