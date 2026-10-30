from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, BasePermission, SAFE_METHODS
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import HttpResponse
from django.utils.text import slugify
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Animal, Evento, Solicitud, SolicitudAdopcion
from .serializers import AnimalSerializer, EventoSerializer, SolicitudSerializer
from .serializers import SolicitudAdopcionSerializer, SolicitudAdopcionGestionSerializer
from .pdf_adopcion import generar_pdf
from . import cuestionario
from rest_framework.decorators import action, api_view, permission_classes
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
        
        Si respondéis a este correo, le llegará directamente a {solicitud.nombre}.
        """

        # La solicitud ya está guardada: si el correo falla, queda en el log y en el panel
        try:
            EmailMessage(
                asunto,
                mensaje,
                settings.DEFAULT_FROM_EMAIL, # Remitente
                [settings.DEFAULT_FROM_EMAIL], # Destinatario (el refugio)
                reply_to=[solicitud.email],
            ).send(fail_silently=False)
        except Exception as e:
            print(f"Error enviando email de la solicitud {solicitud.id}: {e}")
            
            
# --- CUESTIONARIO PRE-ADOPCIÓN ---
@api_view(['GET'])
@permission_classes([AllowAny])
def ver_cuestionario(request, especie):
    definicion = cuestionario.CUESTIONARIOS.get(especie.upper())
    if definicion is None:
        return Response({'error': 'Especie no válida'}, status=404)
    return Response(definicion)


def nombre_pdf(solicitud):
    return f"adopcion-{slugify(solicitud.nombre_animal)}-{slugify(solicitud.nombre)}.pdf"


class SolicitudAdopcionViewSet(viewsets.ModelViewSet):
    queryset = SolicitudAdopcion.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']

    # Cualquiera puede enviar el cuestionario; verlo, gestionarlo o borrarlo es solo del refugio
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAdminUser()]

    def get_serializer_class(self):
        if self.action == 'create':
            return SolicitudAdopcionSerializer
        return SolicitudAdopcionGestionSerializer

    def perform_create(self, serializer):
        solicitud = serializer.save()
        # La solicitud ya está guardada: si el correo falla, se verá igualmente en el panel
        try:
            email = EmailMessage(
                f"🐾 Nueva solicitud de adopción para {solicitud.nombre_animal}",
                f"¡Hola equipo de Villa Pirritx!\n\n"
                f"{solicitud.nombre} ha rellenado el cuestionario pre-adopción para "
                f"{solicitud.nombre_animal} ({solicitud.get_especie_display().lower()}).\n\n"
                f"Email: {solicitud.email}\nTeléfono: {solicitud.telefono}\n\n"
                f"Tenéis el cuestionario completo en el PDF adjunto y en el panel del refugio.\n"
                f"Si respondéis a este correo, le llegará directamente a {solicitud.nombre}.",
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
                reply_to=[solicitud.email],
            )
            email.attach(nombre_pdf(solicitud), generar_pdf(solicitud), 'application/pdf')
            email.send(fail_silently=False)
        except Exception as e:
            print(f"Error enviando email de la solicitud de adopción {solicitud.id}: {e}")

    @action(detail=True, methods=['get'])
    def pdf(self, request, pk=None):
        solicitud = self.get_object()
        respuesta = HttpResponse(generar_pdf(solicitud), content_type='application/pdf')
        respuesta['Content-Disposition'] = f'inline; filename="{nombre_pdf(solicitud)}"'
        return respuesta