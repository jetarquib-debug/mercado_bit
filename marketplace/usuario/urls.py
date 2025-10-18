from django.urls import path
from . import views

app_name = 'usuario'

urlpatterns = [
    path('perfil/', views.perfil_usuario, name='perfil'),
]
