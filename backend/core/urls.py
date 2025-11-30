from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from animales.views import AnimalViewSet

# Configuración del router (crea las URLs automáticamente)
router = DefaultRouter()
router.register(r'animales', AnimalViewSet)

urlpatterns = [
    path('gestion-villapirritx/', admin.site.urls),
    path('api/', include(router.urls)), # Todo lo de la API empezará por /api/
]

# Esto permite ver las fotos subidas mientras estamos en modo desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)