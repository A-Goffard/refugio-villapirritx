from rest_framework import serializers
from .models import Animal
from .models import Solicitud

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = '__all__'
        
class SolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = '__all__'
        # Que nadie pueda marcarla como gestionada desde el formulario público
        read_only_fields = ['gestionada', 'fecha']