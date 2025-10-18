from django.urls import path
from . import views

app_name = 'inicio_sesion'

urlpatterns = [
	path('', views.login_view, name='login'),
]
