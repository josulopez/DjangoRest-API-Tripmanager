from rest_framework import serializers
from .models import Viaje, Itinerario, Actividad, Documento
from django.contrib.auth.models import User

# --- Serializadores de Sub-Elementos ---
class UserCreateSerializer(serializers.ModelSerializer):
    """Serializador para el registro (creación) de nuevos usuarios."""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        # Es CRUCIAL que la contraseña SOLO se pueda escribir (no devolverla)
        extra_kwargs = {'password': {'write_only': True}} 

    def create(self, validated_data):
        # Este método utiliza el 'create_user' de Django, que automáticamente hashea la contraseña.
        user = User.objects.create_user(**validated_data)
        return user
    
class ActividadSerializer(serializers.ModelSerializer):
    """Serializador para las actividades dentro de un itinerario."""
    class Meta:
        model = Actividad
        fields = ['id', 'nombre_actividad', 'hora', 'importancia']

class DocumentoSerializer(serializers.ModelSerializer):
    """Serializador para manejar documentos adjuntos (archivos)."""
    
    archivo_url = serializers.SerializerMethodField() # Para obtener el URL completo del archivo

    class Meta:
        model = Documento
        fields = ['id', 'nombre', 'tipo_documento', 'archivo', 'archivo_url']
        read_only_fields = ['fecha_subida', 'viaje'] # El 'viaje' se asigna en la Vista

    def get_archivo_url(self, obj):
        if obj.archivo:
            # Asegura que se devuelva la URL completa para el frontend
            return obj.archivo.url 
        return None

# --- Serializador Intermedio (Itinerario) ---

class ItinerarioSerializer(serializers.ModelSerializer):
    """Serializador para los itinerarios, incluyendo sus actividades."""
    # Anidamos las actividades dentro del itinerario
    actividades = ActividadSerializer(many=True, read_only=True)
    
    class Meta:
        model = Itinerario
        fields = ['id', 'nombre', 'fecha', 'actividades']
        
# --- Serializador Principal (Viaje) ---

class ViajeSerializer(serializers.ModelSerializer):
    """Serializador principal para la gestión de Viajes."""
    
    # Anidamos itinerarios y documentos
    itinerarios = ItinerarioSerializer(many=True, read_only=True)
    documentos = DocumentoSerializer(many=True, read_only=True)
    
    # Campo para mostrar el nombre de usuario (sólo lectura)
    viajero_username = serializers.CharField(source='viajero.username', read_only=True) 

    class Meta:
        model = Viaje
        fields = [
            'id', 'destino', 'fecha_salida', 'fecha_regreso', 'tipo_viaje', 
            'viajero_username', 'itinerarios', 'documentos'
        ]
        read_only_fields = ['viajero']