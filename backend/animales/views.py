from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from django.core.mail import send_mail
from django.conf import settings
from .models import Animal, Solicitud
from .serializers import AnimalSerializer, SolicitudSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

class AnimalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

# --- NUEVA VISTA PARA SOLICITUDES ---
class SolicitudViewSet(viewsets.ModelViewSet):
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer

    # Cualquiera puede enviar una solicitud desde la web,
    # pero solo el staff puede verlas, editarlas o borrarlas (datos personales)
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAdminUser()]

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
            
            
@api_view(['POST'])
def enviar_solicitud_adopcion(request):
    data = request.data
    
    # 1. Sacamos los datos que nos envía el formulario
    nombre_interesado = data.get('nombre')
    email_interesado = data.get('email')
    telefono = data.get('telefono', 'No indicado')
    nombre_animal = data.get('animal')
    mensaje = data.get('mensaje')

    # 2. Preparamos el cuerpo del correo que TE va a llegar a ti
    asunto = f"🐶 Nueva solicitud de adopción para: {nombre_animal}"
    
    cuerpo_mensaje = f"""
    ¡Hola equipo de Villa Pirritx!
    
    Alguien está interesado en adoptar a {nombre_animal}.
    
    --- DATOS DEL INTERESADO ---
    Nombre: {nombre_interesado}
    Email: {email_interesado}
    Teléfono: {telefono}
    
    --- MENSAJE ---
    {mensaje}
    """

    try:
        # 3. Enviamos el correo usando Brevo
        send_mail(
            asunto,
            cuerpo_mensaje,
            settings.DEFAULT_FROM_EMAIL, # Remitente (Villa Pirritx)
            ['villapirritxanimaliak@gmail.com'], # Destinatario (Tú mismo)
            fail_silently=False,
            # Truco: Si le das a "Responder" en Gmail, responderás al interesado, no a ti mismo
            reply_to=[email_interesado] 
        )
        return Response({'status': 'success', 'message': 'Correo enviado'})
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=500)