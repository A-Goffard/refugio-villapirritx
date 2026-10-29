from rest_framework import serializers
from .models import Animal, Evento
from .models import Solicitud
from .imagenes import optimizar_imagen

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = '__all__'
        read_only_fields = ['created_at']

    def validate_foto(self, foto):
        # Las fotos del móvil pesan varios MB: las reducimos antes de guardarlas
        if foto:
            return optimizar_imagen(foto)
        return foto

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'
        read_only_fields = ['created_at']

    def validate_imagen(self, imagen):
        if imagen:
            return optimizar_imagen(imagen)
        return imagen

class SolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = '__all__'
        # Que nadie pueda marcarla como gestionada desde el formulario público
        read_only_fields = ['gestionada', 'fecha']
