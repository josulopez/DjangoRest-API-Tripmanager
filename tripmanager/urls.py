"""
URL configuration for tripmanager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # RUTAS DE AUTENTICACIÓN (JWT)
    # Endpoint para obtener el par de tokens (acceso y refresco). Usado para Login.
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Endpoint para refrescar el token de acceso cuando expira.
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # RUTAS DE TU API PRINCIPAL
    path('api/', include('api.urls')), 
]
# SERVIR ARCHIVOS MEDIA (¡SOLO PARA DESARROLLO!)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)