from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import os

# Create your models here.
TIPO_VIAJE_CHOICES = [
         ("vacaciones", "Vacaciones"),
         ("negocios", "Negocios"),
]
TIPO_DOCUMENTO_CHOICES = [
    ("boleto", "Boleto de Avión/Tren"),
    ("hotel", "Reserva de Hotel"),
    ("restaurante", "Reserva de Restaurante"),
    ("seguro", "Póliza de Seguro"),
    ("otro", "Otro Documento"),
]
class Viaje(models.Model):
    viajero = models.ForeignKey(User, on_delete=models.CASCADE, related_name='viajes')
    destino = models.CharField(max_length=100)
    fecha_salida = models.DateField()
    fecha_regreso = models.DateField()
    tipo_viaje = models.CharField(max_length=20, choices=TIPO_VIAJE_CHOICES, default="vacaciones")  

    def __str__(self):
        return f"{self.destino} {self.fecha_salida} al {self.fecha_regreso}"

class Itinerario(models.Model):
    viaje = models.ForeignKey('Viaje', on_delete=models.CASCADE, related_name='itinerarios')
    # Campo para identificar el itinerario (ej: "Día 1", "Plan Alternativo")
    nombre = models.CharField(max_length=100)
    # Campo clave: la fecha de este itinerario
    fecha = models.DateField() 
    def __str__(self):
        return f"{self.viaje.destino} - {self.nombre} ({self.fecha})"
    #este campo es mas que nada para relacionar el itinerario con el viaje
    
class Actividad(models.Model):
    itinerario = models.ForeignKey('Itinerario', on_delete=models.CASCADE, related_name='actividades')
    nombre_actividad = models.CharField(max_length=200)
    hora = models.TimeField(null=True, blank=True)
    importancia = models.BooleanField(default=False)   # False para normal, True para importante

    def __str__(self):
        return f"La actividad {self.nombre_actividad} será el {self.fecha}"

class Documento(models.Model):
    # 1. Relación con el Viaje: Se enlaza al viaje al que pertenece
    viaje = models.ForeignKey('Viaje', on_delete=models.CASCADE, related_name='documentos' )# Permite acceder desde Viaje.documentos.all()
    # 2. El Campo para Subir Archivos
    archivo = models.FileField(upload_to='documentos/') # El archivo se guardará en /media/documentos/
    # 3. Datos del Documento
    nombre = models.CharField(max_length=255)
    tipo_documento = models.CharField(max_length=50, choices=TIPO_DOCUMENTO_CHOICES, default='boleto')
    fecha_subida = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"[{self.get_tipo_documento_display()}] {self.nombre} para Viaje a {self.viaje.destino}"
