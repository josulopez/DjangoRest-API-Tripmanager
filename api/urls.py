# api/urls.py
from .views import UserViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ViajeViewSet, 
    ItinerarioViewSet, 
    ActividadViewSet, 
    DocumentoViewSet
)

router = DefaultRouter()
router.register(r'viajes', ViajeViewSet, basename='viaje')
router.register(r'itinerarios', ItinerarioViewSet, basename='itinerario')
router.register(r'actividades', ActividadViewSet, basename='actividad')
router.register(r'documentos', DocumentoViewSet, basename='documento')
router.register(r'users', UserViewSet, basename='user')
urlpatterns = [
    path('', include(router.urls)),
    # ... rutas de autenticación ...
]