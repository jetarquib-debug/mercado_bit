from django.urls import path
from . import views

app_name = 'promociones'

urlpatterns = [
    path('', views.promociones, name='promociones'),
]
