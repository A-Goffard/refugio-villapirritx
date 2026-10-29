from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from animales.views import AnimalViewSet, SolicitudViewSet
from animales.views import enviar_solicitud_adopcion, sesion, iniciar_sesion, cerrar_sesion

# Configuración del router (crea las URLs automáticamente)
router = DefaultRouter()
router.register(r'animales', AnimalViewSet)
router.register(r'solicitudes', SolicitudViewSet)
urlpatterns = [
    path('gestion-villapirritx/', admin.site.urls),
    path('api/', include(router.urls)), # Todo lo de la API empezará por /api/
    path('api/enviar-adopcion/', enviar_solicitud_adopcion),
    path('api/auth/sesion/', sesion),
    path('api/auth/login/', iniciar_sesion),
    path('api/auth/logout/', cerrar_sesion),
]

# Esto permite ver las fotos subidas mientras estamos en modo desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)