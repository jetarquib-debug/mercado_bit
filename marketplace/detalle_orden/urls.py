from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import OrdenViewSet

app_name = 'detalle_orden'

router = DefaultRouter()
router.register(r'api/v1/ordenes', OrdenViewSet, basename='orden')

urlpatterns = [
    path('', include(router.urls)),
]
