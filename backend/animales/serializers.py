from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import validate_email
from rest_framework import serializers
from .models import Animal, Evento
from .models import Solicitud, SolicitudAdopcion
from .imagenes import optimizar_imagen
from . import cuestionario

MAX_RESPUESTA = 3000

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

class SolicitudAdopcionSerializer(serializers.ModelSerializer):
    """Formulario público: solo se envían el animal, las respuestas y la aceptación de privacidad."""
    acepta_privacidad = serializers.BooleanField(write_only=True)

    class Meta:
        model = SolicitudAdopcion
        fields = ['id', 'animal', 'nombre_animal', 'especie', 'nombre', 'email', 'telefono',
                  'respuestas', 'fecha', 'gestionada', 'acepta_privacidad']
        read_only_fields = ['nombre_animal', 'especie', 'nombre', 'email', 'telefono', 'fecha', 'gestionada']
        extra_kwargs = {'animal': {'required': True, 'allow_null': False}}

    def validate_acepta_privacidad(self, acepta):
        if not acepta:
            raise serializers.ValidationError('Tienes que aceptar el tratamiento de tus datos para enviar la solicitud.')
        return acepta

    def validate(self, datos):
        animal = datos['animal']
        recibidas = datos.get('respuestas')
        if not isinstance(recibidas, dict):
            raise serializers.ValidationError({'respuestas': 'Formato incorrecto.'})

        # Solo guardamos las preguntas que existen, como texto y con un tamaño razonable
        respuestas, faltan = {}, {}
        for pregunta in cuestionario.preguntas(animal.especie):
            clave = pregunta['clave']
            valor = str(recibidas.get(clave) or '').strip()[:MAX_RESPUESTA]
            if valor:
                respuestas[clave] = valor
            elif pregunta['obligatoria']:
                faltan[clave] = 'Este campo es obligatorio.'
        if faltan:
            raise serializers.ValidationError({'respuestas': faltan})

        try:
            validate_email(respuestas['email'])
        except DjangoValidationError:
            raise serializers.ValidationError({'respuestas': {'email': 'Escribe un email válido.'}})

        datos.pop('acepta_privacidad')
        datos.update(
            respuestas=respuestas,
            especie=animal.especie,
            nombre_animal=animal.nombre,
            nombre=respuestas['nombre'][:150],
            email=respuestas['email'],
            telefono=respuestas['telefono'][:50],
        )
        return datos

class SolicitudAdopcionGestionSerializer(serializers.ModelSerializer):
    """Panel del refugio: se ve todo, pero solo se puede cambiar si está gestionada."""
    class Meta:
        model = SolicitudAdopcion
        fields = ['id', 'animal', 'nombre_animal', 'especie', 'nombre', 'email', 'telefono',
                  'respuestas', 'fecha', 'gestionada']
        read_only_fields = [f for f in fields if f != 'gestionada']
