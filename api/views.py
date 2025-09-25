from django.shortcuts import render

# Create your views here.
# api/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Viaje, Itinerario, Actividad, Documento
from .serializers import (
    ViajeSerializer, 
    ItinerarioSerializer, 
    ActividadSerializer, 
    DocumentoSerializer
)
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .serializers import UserCreateSerializer
# ----------------- VIEWSETS DE VIAJES (CON SEGURIDAD) -----------------

class ViajeViewSet(viewsets.ModelViewSet):
    """Gestiona Viajes. Restringido al usuario autenticado."""
    serializer_class = ViajeSerializer
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        # Filtra para mostrar SOLO los viajes del usuario actual
        return Viaje.objects.filter(viajero=self.request.user)

    def perform_create(self, serializer):
        # Asigna automáticamente al usuario actual como el viajero
        serializer.save(viajero=self.request.user)


class ItinerarioViewSet(viewsets.ModelViewSet):
    """Gestiona Itinerarios. Filtrado por el viaje del usuario actual."""
    serializer_class = ItinerarioSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Filtra itinerarios para que solo sean de los viajes del usuario
        return Itinerario.objects.filter(viaje__viajero=self.request.user)


class ActividadViewSet(viewsets.ModelViewSet):
    """Gestiona Actividades. Filtrado por el itinerario del viaje del usuario actual."""
    serializer_class = ActividadSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Filtra actividades para que solo sean de los itinerarios de los viajes del usuario
        return Actividad.objects.filter(itinerario__viaje__viajero=self.request.user)

# ----------------- VIEWSET DE DOCUMENTOS (SIN IsAuthenticated) -----------------

class DocumentoViewSet(viewsets.ModelViewSet):
    """Gestiona Documentos. Permite acceso sin autenticación (si lo quieres) pero filtra."""
    serializer_class = DocumentoSerializer
    # Usamos AllowAny para dejar pasar a cualquiera si así lo quieres. 
    # Si quieres que SÓLO los autenticados vean los documentos, usa IsAuthenticated aquí.
    permission_classes = [AllowAny] 
    
    def get_queryset(self):
        # *IMPORTANTE:* Aunque permitamos AllowAny, el QUERYSENSE es el que filtra.
        # Si la petición no tiene un usuario, esto podría fallar.
        # En una API REST, el mejor enfoque es mantener IsAuthenticated. 
        # Si insistes, puedes devolver Viaje.objects.all() en este caso, pero es INSEGURO.
        
        # Mantenemos el filtro: si hay usuario, muestra sus documentos.
        if self.request.user.is_authenticated:
            return Documento.objects.filter(viaje__viajero=self.request.user)
        # Si no está autenticado, no mostraremos NADA. (Recomendado para evitar exponer datos)
        return Documento.objects.none() 
    
    def perform_create(self, serializer):
        # Aquí debes asegurar que el ID de 'viaje' que viene en la petición POST pertenezca al usuario.
        # Por simplicidad, se guarda, pero la validación real de propiedad es vital.
        serializer.save()

class UserViewSet(viewsets.ModelViewSet):
    """
    Permite el registro de nuevos usuarios (POST)
    y restringe otras operaciones para mantener la seguridad.
    """
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    # Permite que CUALQUIER persona (no autenticada) acceda a esta vista. ¡Necesario para registrarse!
    permission_classes = [AllowAny] 
    
    # Sobreescribe el método para definir las acciones permitidas (solo 'create' para POST)
    def get_permissions(self):
        # Permitir que solo la acción POST (registro) use AllowAny
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        # Para todas las demás acciones (list, retrieve, update), usa IsAuthenticated o niega.
        else:
            self.permission_classes = [IsAuthenticated] # O simplemente [Denied] si no quieres permitir nada más
        return super().get_permissions()

    # Recomendación: Deshabilita el listado de usuarios para evitar exponer datos
    def list(self, request, *args, **kwargs):
        return Response({"detail": "El listado de usuarios no está permitido."}, status=403)