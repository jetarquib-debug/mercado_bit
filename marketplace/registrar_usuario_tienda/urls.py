from django.urls import path
from . import views

app_name = 'registrar_usuario_tienda'

urlpatterns = [
    path('usuario/', views.registrar_usuario, name='registro_usuario'),
    path('tienda/', views.registrar_tienda, name='registro_tienda'),
    path('exito/', views.registro_exito, name='registro_exito'),
]
