
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .viewsets import PromocionViewSet

app_name = 'promociones'

router = DefaultRouter()
router.register(r'api/promociones', PromocionViewSet, basename='promocion')

urlpatterns = [
    path('', views.promociones, name='promociones'),
    path('', include(router.urls)),
]
