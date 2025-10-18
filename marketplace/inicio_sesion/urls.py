from django.urls import path
from . import views

app_name = 'inicio_sesion'

urlpatterns = [
	path('login/', views.login_usuario, name='login'),
	path('logout/', views.logout_usuario, name='logout'),
]
