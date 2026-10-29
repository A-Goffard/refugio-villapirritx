from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, BasePermission, SAFE_METHODS
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Animal, Evento, Solicitud
from .serializers import AnimalSerializer, EventoSerializer, SolicitudSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


class EsStaffOSoloLectura(BasePermission):
    """Todo el mundo puede ver; solo el equipo del refugio puede cambiar cosas."""
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_staff


class BorraImagenViejaMixin:
    """Al cambiar, quitar o borrar la imagen de un registro, elimina el archivo viejo del disco."""
    campo_imagen = None

    def perform_update(self, serializer):
        anterior = getattr(serializer.instance, self.campo_imagen).name
        objeto = serializer.save()
        imagen = getattr(objeto, self.campo_imagen)
        if anterior and anterior != imagen.name:
            imagen.storage.delete(anterior)

    def perform_destroy(self, instance):
        imagen = getattr(instance, self.campo_imagen)
        if imagen:
            imagen.storage.delete(imagen.name)
        instance.delete()


class AnimalViewSet(BorraImagenViejaMixin, viewsets.ModelViewSet):
    queryset = Animal.objects.order_by('-created_at')
    serializer_class = AnimalSerializer
    permission_classes = [EsStaffOSoloLectura]
    campo_imagen = 'foto'


class EventoViewSet(BorraImagenViejaMixin, viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [EsStaffOSoloLectura]
    campo_imagen = 'imagen'


# --- SESIÓN PARA EL PANEL DE GESTIÓN ---
@ensure_csrf_cookie
@api_view(['GET'])
@permission_classes([AllowAny])
def sesion(request):
    # Además de decir quién está conectado, deja la cookie CSRF para los POST
    if request.user.is_staff:
        return Response({'usuario': request.user.get_username()})
    return Response({'usuario': None})


@api_view(['POST'])
@permission_classes([AllowAny])
def iniciar_sesion(request):
    usuario = authenticate(
        request,
        username=request.data.get('usuario'),
        password=request.data.get('contrasena'),
    )
    if usuario is None or not usuario.is_staff:
        return Response({'error': 'Usuario o contraseña incorrectos'}, status=400)
    login(request, usuario)
    return Response({'usuario': usuario.get_username()})


@api_view(['POST'])
@permission_classes([AllowAny])
def cerrar_sesion(request):
    logout(request)
    return Response({'usuario': None})

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