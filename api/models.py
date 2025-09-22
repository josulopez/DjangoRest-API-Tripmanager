from django.db import models

# Create your models here.
 class Viaje(models.Model):
     destino = models.CharField(max_length=100)
     fecha_salida = models.DateField()
     fecha_regreso = models.DateField()
     tipo_viaje = models.BooleanField(default=False)  # False para Vacaciones, True para Negociosl

     def __str__(self):
         return f"{self.destino} {self.fecha_salida} al {self.fecha_regreso}"