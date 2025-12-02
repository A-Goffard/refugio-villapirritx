from rest_framework import viewsets
from django.core.mail import send_mail
from django.conf import settings
from .models import Animal, Solicitud
from .serializers import AnimalSerializer, SolicitudSerializer

class AnimalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

# --- NUEVA VISTA PARA SOLICITUDES ---
class SolicitudViewSet(viewsets.ModelViewSet):
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer

    # Sobreescribimos el método de guardar para enviar el mail
    def perform_create(self, serializer):
        solicitud = serializer.save()
        
        # Preparamos el email
        asunto = f"Nueva solicitud de {solicitud.get_tipo_display()}: {solicitud.nombre}"
        mensaje = f"""
        ¡Hola equipo Villa Pirritx!
        
        Habéis recibido una nueva solicitud desde la web.
        
        Tipo: {solicitud.get_tipo_display()}
        Nombre: {solicitud.nombre}
        Email: {solicitud.email}
        Teléfono: {solicitud.telefono}
        
        Mensaje:
        {solicitud.mensaje}
        
        Entrad al panel de administración para gestionarla.
        """
        
        try:
            send_mail(
                asunto,
                mensaje,
                settings.DEFAULT_FROM_EMAIL, # Remitente
                [settings.DEFAULT_FROM_EMAIL], # Destinatario (el refugio)
                fail_silently=True,
            )
        except Exception as e:
            print(f"Error enviando email: {e}")